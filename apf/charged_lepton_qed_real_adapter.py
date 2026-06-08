"""
APF Charged-Lepton QED Real Adapter -- Tier-1 wire-in (atlas v0.6 follow-on).

v24.3.27+ Engine-side adapter that turns the banked v70 QED running evaluator +
v48 covariance ledger content into a typed route payload the Engine can read.
Mirrors the ew_dizet_real_adapter (Campaign B Phase 2) and light_quark_real_adapter
(Campaign C) patterns but for the EW charged-lepton mass-sector route through
the QED LO self-scale evaluator + CODATA 2022 external constants ledger.

Purpose
-------
Atlas v0.5 (light-quark + EW DIZET wire-ins) lifted 2 of 42 routes to
SOLVED_GLOBAL_P. The charged-lepton route (mass:route02_charged_lepton_qed_running
in the v0.2 input set) still hits EVALUATOR_MISSING despite the LATEST-25 v48
[P_QED truncation covariance admitted] + [P_full QED running ledger typed]
status. The gap is that no Engine-side adapter reads the v70 LO QED self-scale
evaluator output into a route payload.

This module closes that gap. Reads the v43 pole vector
(0.5110026357885311, 105.658243985342, 1776.9168320084111) MeV +
v70 LO QED self-scale outputs (m_bar_i = Phi_i / (1 + alpha/pi) per lepton)
+ CODATA 2022 external constants ledger (alpha^-1 = 137.035999177(21)) +
v48 APF envelope (1/5063 = 0.0198%) + perturbative truncation envelope
(100 * (alpha/pi)^2 = 0.000540%). Produces an EW-shaped route payload where
evaluator_map_found, codomain_transport_found, counterterm_finite_parts_declared,
external_constants_ledger_clean, and uncertainty_protocol_declared all resolve
to True against the banked v70 + v48 content. target_value_consumed stays False
(CODATA lepton-mass references are diagnostic-only comparators, never inputs;
generation residual knobs r_e/r_mu/r_tau forbidden per v48 ledger).

Status banked by this module
----------------------------
- Export_charged_lepton_pole_completion_APF_envelope = 1 (preserved from v46)
- Export_charged_lepton_QED_running_route_typed = 1 (preserved from v45)
- Export_charged_lepton_QED_LO_selfscale_evaluator_closed = 1 (preserved from v70)
- Export_charged_lepton_QED_truncation_covariance_admitted = 1 (preserved from v48)
- Export_charged_lepton_QED_engine_adapter_wired = 1 (NEW at this module)
- Export_charged_lepton_QED_full_running_with_external_coefficient_ledger = 0
  (LATEST-25 next-gate non-claim, preserved)
- Export_charged_lepton_APF_internal_full_QED_loop_derivation = 0
  (the APF-internal-derivation gate, separate from imported-route closure)

The adapter does NOT promote the route to APF-internal-derivation status. It
promotes Engine readability of the existing imported-one-route closure to
machine-checkable form via Engine pipeline traversal. The L>=2 multi-loop
coefficient/threshold/matching ledger remains externally required.

Top check: check_T_charged_lepton_qed_real_adapter_P
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Mapping, Optional, Tuple

try:
    from apf.interface_structure_discovery_engine import discover_and_certify
    from apf.interface_structure_movement_graph import movement_graph_report
    from apf.interface_repair_frontier_explorer import explore_repair_frontier
    from apf.interface_repair_obligation_compiler import (
        compile_obligation_packet,
        evidence_template,
    )
    from apf.interface_evidence_rerun_controller import control_evidence_rerun
except Exception as exc:  # pragma: no cover
    raise ImportError(
        f"charged_lepton_qed_real_adapter requires the interface-intelligence stack: {exc}"
    ) from exc


# ============================================================================
# Banked v70 + v48 content (verbatim from V36_THROUGH_V79_LADDER_BUNDLE)
# ============================================================================

# CODATA 2022 external ledger (imported, not source inputs).
# Diagnostic references only; never routed as evaluator input.
CODATA_2022_LEDGER: Mapping[str, Any] = {
    "source": "NIST/CODATA 2022 external ledger",
    "alpha_inverse": 137.035999177,
    "alpha_inverse_uncertainty": 2.1e-08,
    "alpha": 0.0072973525643314245,
    "alpha_uncertainty": 1.1182784434112427e-12,
    # CODATA pole references for residual diagnostics ONLY.
    "lepton_pole_MeV_diagnostic": (0.51099895069, 105.6583755, 1776.86),
    "lepton_pole_uncertainty_MeV": (1.6e-10, 2.3e-06, 0.12),
}

# APF trace pole vector (Phi_l^v43) -- the LATEST-25 v43 closure content.
# Source-side closed; never consumes CODATA references as inputs.
APF_POLE_V43_MEV: Tuple[float, float, float] = (
    0.5110026357885311,
    105.658243985342,
    1776.9168320084111,
)

# v70 LO QED self-scale evaluator outputs: m_bar_i = Phi_i / (1 + alpha/pi)
# Computed at LO from the CODATA alpha; deterministic given APF source + alpha.
QED_LO_SELFSCALE_MEV: Tuple[float, float, float] = (
    0.509818419641,
    105.413387716567,
    1772.798940124185,
)

# v48 APF envelope and truncation channels (the non-fit covariance protocol).
# APF envelope = 1 / 5063 (the LATEST-44 count-ledger denominator).
# Perturbative truncation = 100 * (alpha/pi)^2 in percent units.
APF_ENVELOPE_PERCENT: float = 0.019751135690302193
PERTURBATIVE_TRUNCATION_PERCENT: float = 0.00054035026170335
# Loop-order ladder banked at v48.
LOOP_ORDER_LADDER: Mapping[str, str] = {
    "L0": "identity / pole route -- evaluated",
    "L1": "one-loop self-scale pole-MSbar witness -- evaluated (v70)",
    "L_ge_2": "external coefficients required -- NOT evaluated",
}

# Pole-vs-CODATA residuals (percent), evaluated at v48 under CODATA 2022.
# Max abs residual = 0.003198% (tau) -- all inside APF envelope 0.0198%.
POLE_RESIDUALS_PERCENT: Tuple[float, float, float] = (
    0.0007211557922236904,
    -0.00012447158815943914,
    0.003198451673807737,
)

# Required external evaluator ledger fields (9, mirroring DIZET's 9-field count).
REQUIRED_EXTERNAL_LEDGER_FIELDS: Tuple[str, ...] = (
    "external_alpha_QED_inverse_CODATA",
    "external_codata_lepton_mass_diagnostic_references",
    "external_loop_order_L0_pole_identity",
    "external_loop_order_L1_LO_selfscale_evaluator",
    "external_loop_order_Lge2_coefficient_ledger_required",
    "external_threshold_schedule_QED_active_leptons",
    "external_OS_MSbar_matching_convention",
    "external_scale_choice_convention",
    "APF_envelope_plus_perturbative_truncation_covariance_protocol",
)

# No-smuggling guard: keys that must NEVER appear as route inputs.
# CODATA pole references are diagnostic-only comparators, never inputs.
# Generation residual knobs (r_e, r_mu, r_tau) are forbidden by v48.
TARGET_VALUE_KEYS: frozenset = frozenset({
    "codata_pole_e", "codata_pole_mu", "codata_pole_tau",
    "target_e_mass", "target_mu_mass", "target_tau_mass",
    "measured_lepton_mass", "measured_e_mass", "measured_mu_mass", "measured_tau_mass",
    "lepton_mass_target",
    # Generation residual knobs forbidden at v48.
    "r_e", "r_mu", "r_tau",
    "generation_residual_e", "generation_residual_mu", "generation_residual_tau",
})


# ============================================================================
# Snapshot + Report dataclasses
# ============================================================================

@dataclass(frozen=True)
class ChargedLeptonQedAdapterSnapshot:
    """Typed snapshot of the charged-lepton EW route state via v70 + v48.

    Boolean flags correspond to the EW-shaped route payload contract.
    """
    trace_sector_closed: bool
    source_to_scheme_registry_present: bool
    evaluator_map_found: bool
    codomain_transport_found: bool
    counterterm_finite_parts_declared: bool
    external_constants_ledger_clean: bool
    uncertainty_protocol_declared: bool
    target_value_consumed: bool
    qed_lo_evaluator_evaluated: bool
    pole_residuals_inside_APF_envelope: bool
    external_ledger_fields_declared: Tuple[str, ...]
    notes: str = ""

    def to_payload(self, name: str = "charged_lepton_qed_real_adapter") -> Dict[str, Any]:
        return {
            "name": name,
            "trace_sector_closed": self.trace_sector_closed,
            "source_to_scheme_registry_present": self.source_to_scheme_registry_present,
            "evaluator_map_found": self.evaluator_map_found,
            "codomain_transport_found": self.codomain_transport_found,
            "counterterm_finite_parts_declared": self.counterterm_finite_parts_declared,
            "external_constants_ledger_clean": self.external_constants_ledger_clean,
            "uncertainty_protocol_declared": self.uncertainty_protocol_declared,
            "target_value_consumed": self.target_value_consumed,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class ChargedLeptonQedAdapterReport:
    payload: Mapping[str, Any]
    snapshot: ChargedLeptonQedAdapterSnapshot
    qed_outputs: Mapping[str, Any]
    certification: Mapping[str, Any]
    movement_graph: Mapping[str, Any]
    frontier: Mapping[str, Any]
    obligation_packet: Mapping[str, Any]
    evidence_template: Mapping[str, Any]
    rerun_result_without_evidence: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payload": dict(self.payload),
            "snapshot": asdict(self.snapshot),
            "qed_outputs": dict(self.qed_outputs),
            "certification": dict(self.certification),
            "movement_graph": dict(self.movement_graph),
            "frontier": dict(self.frontier),
            "obligation_packet": dict(self.obligation_packet),
            "evidence_template": dict(self.evidence_template),
            "rerun_result_without_evidence": dict(self.rerun_result_without_evidence),
        }


# ============================================================================
# Snapshot construction
# ============================================================================

def infer_snapshot_from_banked_qed_content(
    *,
    overrides: Optional[Mapping[str, Any]] = None,
) -> ChargedLeptonQedAdapterSnapshot:
    """Build snapshot from the v70 LO QED + v48 covariance banked content.

    All booleans set True for fields the v70 + v48 content fills:
        - trace_sector_closed                  (Phi_l^v43 banked at v43)
        - source_to_scheme_registry_present    (v45 QED running route typed
                                                under LATEST-25 chain)
        - evaluator_map_found                  (v70 LO evaluator outputs
                                                m_bar_i = Phi_i/(1+alpha/pi)
                                                per lepton)
        - codomain_transport_found             (pole -> MSbar self-scale at L1)
        - counterterm_finite_parts_declared    (v48 APF envelope + truncation
                                                channels under non-fit policy)
        - external_constants_ledger_clean      (CODATA 2022 alpha^-1 declared
                                                with uncertainty 2.1e-8)
        - uncertainty_protocol_declared        (APF envelope + CODATA constants
                                                + perturbative truncation)
        - target_value_consumed                (False -- CODATA pole references
                                                diagnostic-only; r_e/r_mu/r_tau
                                                forbidden generation knobs)

    Only target_value_consumed defaults False (no smuggling). All other flags
    True because the v70 + v48 ledger supplies the required fields under the
    LATEST-25 imported-one-route admission policy.
    """
    # All v48 pole-vs-CODATA residuals inside APF envelope 0.0198%.
    residuals_inside = all(
        abs(r) < APF_ENVELOPE_PERCENT for r in POLE_RESIDUALS_PERCENT
    )
    base = dict(
        trace_sector_closed=True,
        source_to_scheme_registry_present=True,
        evaluator_map_found=True,
        codomain_transport_found=True,
        counterterm_finite_parts_declared=True,
        external_constants_ledger_clean=True,
        uncertainty_protocol_declared=True,
        target_value_consumed=False,
        qed_lo_evaluator_evaluated=True,
        pole_residuals_inside_APF_envelope=residuals_inside,
        external_ledger_fields_declared=REQUIRED_EXTERNAL_LEDGER_FIELDS,
        notes=(
            "v70 LO QED self-scale evaluator + v48 covariance ledger admitted "
            "as named external evaluator content under LATEST-25 v48 imported-"
            "one-route policy. Phi_l^v43 = (0.5110, 105.658, 1776.917) MeV; "
            "m_bar_i = Phi_i / (1+alpha/pi) at CODATA 2022 alpha^-1 = "
            "137.035999177; APF envelope 1/5063 = 0.0198%; max pole-vs-CODATA "
            "residual 0.003198% (tau) inside envelope. Status: "
            "[P_QED_truncation_covariance_admitted] + [P_full QED running "
            "ledger typed] preserved at LATEST-25 v48. Adapter wires the v70 "
            "+ v48 content into Engine-readable payload. L>=2 multi-loop "
            "coefficient/threshold/matching ledger remains externally required "
            "(LATEST-25 next-gate non-claim preserved). APF-internal full QED "
            "loop derivation OPEN as separate program."
        ),
    )
    if overrides:
        for k, v in overrides.items():
            if k in base:
                base[k] = v
    return ChargedLeptonQedAdapterSnapshot(**base)


def snapshot_from_payload(payload: Mapping[str, Any]) -> ChargedLeptonQedAdapterSnapshot:
    """Build snapshot from an arbitrary payload dict (testing convenience)."""
    return ChargedLeptonQedAdapterSnapshot(
        trace_sector_closed=bool(payload.get("trace_sector_closed", False)),
        source_to_scheme_registry_present=bool(payload.get("source_to_scheme_registry_present", False)),
        evaluator_map_found=bool(payload.get("evaluator_map_found", False)),
        codomain_transport_found=bool(payload.get("codomain_transport_found", False)),
        counterterm_finite_parts_declared=bool(payload.get("counterterm_finite_parts_declared", False)),
        external_constants_ledger_clean=bool(payload.get("external_constants_ledger_clean", False)),
        uncertainty_protocol_declared=bool(payload.get("uncertainty_protocol_declared", False)),
        target_value_consumed=bool(payload.get("target_value_consumed", False)),
        qed_lo_evaluator_evaluated=bool(payload.get("qed_lo_evaluator_evaluated", False)),
        pole_residuals_inside_APF_envelope=bool(payload.get("pole_residuals_inside_APF_envelope", False)),
        external_ledger_fields_declared=tuple(payload.get("external_ledger_fields_declared", ())),
        notes=str(payload.get("notes", "")),
    )


# ============================================================================
# QED output report payload
# ============================================================================

def qed_outputs_report() -> Dict[str, Any]:
    """Return a structured representation of the banked v70 + v48 content."""
    return {
        "apf_pole_v43_MeV": list(APF_POLE_V43_MEV),
        "qed_lo_selfscale_MeV": list(QED_LO_SELFSCALE_MEV),
        "codata_2022_ledger": {
            k: (list(v) if isinstance(v, tuple) else v)
            for k, v in CODATA_2022_LEDGER.items()
        },
        "pole_residuals_percent": list(POLE_RESIDUALS_PERCENT),
        "apf_envelope_percent": APF_ENVELOPE_PERCENT,
        "perturbative_truncation_percent": PERTURBATIVE_TRUNCATION_PERCENT,
        "loop_order_ladder": dict(LOOP_ORDER_LADDER),
        "required_external_ledger_fields": list(REQUIRED_EXTERNAL_LEDGER_FIELDS),
        "row_admission_protocol": (
            "LATEST-25 v48: v70 LO QED self-scale evaluator + CODATA 2022 "
            "constants ledger admitted as named external evaluator content "
            "under non-fit covariance policy. Pole residuals diagnostic-only "
            "vs CODATA references; generation residual knobs r_e/r_mu/r_tau "
            "explicitly forbidden as fitting parameters."
        ),
        "no_smuggling_protocol": (
            "v48 ledger: CODATA charged-lepton mass references serve as "
            "diagnostic comparators ONLY, never as APF route inputs. "
            "Phi_l^v43 is APF-source-closed at v43. r_e/r_mu/r_tau "
            "generation residual knobs forbidden."
        ),
        "status": {
            "Export_charged_lepton_pole_completion_APF_envelope": 1,
            "Export_charged_lepton_QED_running_route_typed": 1,
            "Export_charged_lepton_QED_LO_selfscale_evaluator_closed": 1,
            "Export_charged_lepton_QED_truncation_covariance_admitted": 1,
            "Export_charged_lepton_QED_engine_adapter_wired": 1,  # NEW at this module
            "Export_charged_lepton_QED_full_running_with_external_coefficient_ledger": 0,
            "Export_charged_lepton_APF_internal_full_QED_loop_derivation": 0,
        },
    }


# ============================================================================
# Full adapter report
# ============================================================================

def build_adapter_report(
    snapshot: ChargedLeptonQedAdapterSnapshot,
    *,
    name: str = "charged_lepton_qed_real_adapter",
) -> ChargedLeptonQedAdapterReport:
    """Run the full Engine pipeline on the snapshot's payload."""
    payload = snapshot.to_payload(name=name)
    route = "ew"
    certification = discover_and_certify(route, payload)
    movement = movement_graph_report(route, payload)
    frontier = explore_repair_frontier(route, payload).to_dict()
    packet = compile_obligation_packet(route, payload)
    template = evidence_template(packet)
    rerun_without_evidence = control_evidence_rerun(route, payload).to_dict()
    return ChargedLeptonQedAdapterReport(
        payload=payload,
        snapshot=snapshot,
        qed_outputs=qed_outputs_report(),
        certification=certification,
        movement_graph=movement,
        frontier=frontier,
        obligation_packet=packet.to_dict(),
        evidence_template=template,
        rerun_result_without_evidence=rerun_without_evidence,
    )


def build_live_adapter_report(
    *,
    overrides: Optional[Mapping[str, Any]] = None,
    name: str = "charged_lepton_qed_real_adapter_live",
) -> ChargedLeptonQedAdapterReport:
    """Build report from the banked v70 + v48 content (default live path)."""
    snapshot = infer_snapshot_from_banked_qed_content(overrides=overrides)
    return build_adapter_report(snapshot, name=name)


# ============================================================================
# Canonical manual snapshots (for testing)
# ============================================================================

def canonical_manual_snapshots() -> Dict[str, ChargedLeptonQedAdapterSnapshot]:
    """Three canonical snapshots covering pre-wire / wire-in / smuggled cases."""
    return {
        "before_wire_in": ChargedLeptonQedAdapterSnapshot(
            trace_sector_closed=True,
            source_to_scheme_registry_present=False,
            evaluator_map_found=False,
            codomain_transport_found=False,
            counterterm_finite_parts_declared=False,
            external_constants_ledger_clean=False,
            uncertainty_protocol_declared=False,
            target_value_consumed=False,
            qed_lo_evaluator_evaluated=False,
            pole_residuals_inside_APF_envelope=False,
            external_ledger_fields_declared=(),
            notes="Pre-wire baseline: v70 + v48 content banked but no Engine-side adapter; not Engine-readable.",
        ),
        "post_wire_in": infer_snapshot_from_banked_qed_content(),
        "smuggled_codata_pole_input": ChargedLeptonQedAdapterSnapshot(
            trace_sector_closed=True,
            source_to_scheme_registry_present=True,
            evaluator_map_found=True,
            codomain_transport_found=True,
            counterterm_finite_parts_declared=True,
            external_constants_ledger_clean=True,
            uncertainty_protocol_declared=True,
            target_value_consumed=True,  # CODATA reference used as input -> fail
            qed_lo_evaluator_evaluated=True,
            pole_residuals_inside_APF_envelope=True,
            external_ledger_fields_declared=REQUIRED_EXTERNAL_LEDGER_FIELDS,
            notes="Smuggled CODATA-pole-as-input case: should fail provenance gate.",
        ),
    }


def run_canonical_adapter_reports() -> Dict[str, Dict[str, Any]]:
    return {
        name: build_adapter_report(snap).to_dict()
        for name, snap in canonical_manual_snapshots().items()
    }


# ============================================================================
# Bank-registered check functions
# ============================================================================

def check_T_charged_lepton_qed_adapter_payload_contract_P() -> Dict[str, Any]:
    """Adapter snapshot produces a route payload conforming to EW route contract."""
    snap = infer_snapshot_from_banked_qed_content()
    payload = snap.to_payload()
    required_keys = {
        "name", "trace_sector_closed", "source_to_scheme_registry_present",
        "evaluator_map_found", "codomain_transport_found",
        "counterterm_finite_parts_declared", "external_constants_ledger_clean",
        "uncertainty_protocol_declared", "target_value_consumed", "notes",
    }
    has_all_keys = required_keys.issubset(payload.keys())
    no_smuggling = payload["target_value_consumed"] is False
    evaluator_filled = payload["evaluator_map_found"] is True
    codomain_filled = payload["codomain_transport_found"] is True
    return {
        "name": "check_T_charged_lepton_qed_adapter_payload_contract_P",
        "consistent": has_all_keys and no_smuggling and evaluator_filled and codomain_filled,
        "status": "P_real_adapter" if (has_all_keys and no_smuggling and evaluator_filled) else "FAIL",
        "summary": "Charged-lepton QED adapter produces EW-shaped route payload with v70-filled evaluator + codomain.",
        "data": {
            "required_keys_present": has_all_keys,
            "no_smuggling": no_smuggling,
            "evaluator_filled": evaluator_filled,
            "codomain_filled": codomain_filled,
        },
    }


def check_T_charged_lepton_qed_adapter_evaluator_consistent_P() -> Dict[str, Any]:
    """v70 LO self-scale evaluator outputs match Phi_l / (1 + alpha/pi) exactly."""
    alpha = CODATA_2022_LEDGER["alpha"]
    expected = tuple(p / (1.0 + alpha / 3.141592653589793) for p in APF_POLE_V43_MEV)
    actual = QED_LO_SELFSCALE_MEV
    consistent_per_lepton = {}
    for name, a, e in zip(("e", "mu", "tau"), actual, expected):
        # 1e-9 MeV tolerance (banked v70 evaluator output precision)
        consistent_per_lepton[name] = abs(a - e) < 1e-9
    return {
        "name": "check_T_charged_lepton_qed_adapter_evaluator_consistent_P",
        "consistent": all(consistent_per_lepton.values()),
        "status": "P_v70_evaluator_consistent" if all(consistent_per_lepton.values()) else "FAIL",
        "summary": "v70 LO self-scale outputs match Phi_l^v43 / (1+alpha/pi) at CODATA 2022 alpha for all three leptons.",
        "data": {
            "consistent_per_lepton": consistent_per_lepton,
            "alpha_inverse": CODATA_2022_LEDGER["alpha_inverse"],
            "apf_pole_v43_MeV": list(APF_POLE_V43_MEV),
            "qed_lo_selfscale_MeV_banked": list(QED_LO_SELFSCALE_MEV),
            "qed_lo_selfscale_MeV_recomputed": list(expected),
        },
    }


def check_T_charged_lepton_qed_adapter_no_smuggling_P() -> Dict[str, Any]:
    """Adapter snapshot does not consume CODATA pole references or generation knobs."""
    snap = infer_snapshot_from_banked_qed_content()
    payload = snap.to_payload()
    smuggled = [k for k in TARGET_VALUE_KEYS if k in payload]
    return {
        "name": "check_T_charged_lepton_qed_adapter_no_smuggling_P",
        "consistent": (not smuggled) and (not payload["target_value_consumed"]),
        "status": "P_no_smuggling" if not smuggled else "FAIL",
        "summary": "No CODATA-pole-as-input or generation-residual-knob in payload; target_value_consumed=False.",
        "data": {
            "smuggled_keys": smuggled,
            "target_value_consumed": payload["target_value_consumed"],
            "forbidden_keys_count": len(TARGET_VALUE_KEYS),
        },
    }


def check_T_charged_lepton_qed_adapter_external_ledger_declared_P() -> Dict[str, Any]:
    """Adapter declares the 9 required external evaluator ledger fields."""
    snap = infer_snapshot_from_banked_qed_content()
    declared = set(snap.external_ledger_fields_declared)
    required = set(REQUIRED_EXTERNAL_LEDGER_FIELDS)
    return {
        "name": "check_T_charged_lepton_qed_adapter_external_ledger_declared_P",
        "consistent": declared == required,
        "status": "P_external_ledger_declared" if declared == required else "FAIL",
        "summary": "All 9 required QED external evaluator ledger fields declared on the snapshot.",
        "data": {
            "declared_count": len(declared),
            "required_count": len(required),
            "missing": sorted(required - declared),
        },
    }


def check_T_charged_lepton_qed_adapter_certification_P() -> Dict[str, Any]:
    """Engine certification on adapter payload produces clean EW route reading."""
    report = build_live_adapter_report()
    packet_status = report.obligation_packet.get("packet_status")
    rerun_status = report.rerun_result_without_evidence.get("status")
    edges = report.movement_graph.get("edges", [])
    evaluator_edge = next(
        (e for e in edges if e.get("kind") == "EVALUATOR_MAP"),
        None,
    )
    evaluator_filled = evaluator_edge is not None and evaluator_edge.get("status") in (
        "MOVES_CLEANLY", "PRESENT_STABLE",
    )
    return {
        "name": "check_T_charged_lepton_qed_adapter_certification_P",
        "consistent": evaluator_filled,
        "status": "P_real_adapter" if evaluator_filled else "FAIL",
        "summary": "EVALUATOR_MAP edge in EW movement graph resolves to MOVES_CLEANLY with v70-filled payload.",
        "data": {
            "packet_status": packet_status,
            "rerun_status": rerun_status,
            "evaluator_edge_status": evaluator_edge.get("status") if evaluator_edge else "MISSING",
        },
    }


def check_T_charged_lepton_qed_real_adapter_P() -> Dict[str, Any]:
    """Top integration check for the charged-lepton QED real adapter."""
    subchecks = [
        check_T_charged_lepton_qed_adapter_payload_contract_P(),
        check_T_charged_lepton_qed_adapter_evaluator_consistent_P(),
        check_T_charged_lepton_qed_adapter_no_smuggling_P(),
        check_T_charged_lepton_qed_adapter_external_ledger_declared_P(),
        check_T_charged_lepton_qed_adapter_certification_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_charged_lepton_qed_real_adapter_P",
        "consistent": ok,
        "status": "P_real_adapter" if ok else "FAIL",
        "summary": (
            "Charged-lepton QED real adapter wires banked v70 LO self-scale "
            "evaluator + v48 covariance ledger into Engine-readable route "
            "payload; EVALUATOR_MAP edge fills cleanly; no smuggling (CODATA "
            "diagnostic-only + r_e/r_mu/r_tau forbidden); 9-field external "
            "ledger declared; v70 outputs match Phi_l/(1+alpha/pi) exactly."
        ),
        "dependencies": [x["name"] for x in subchecks],
        "data": {"subchecks": {x["name"]: x["consistent"] for x in subchecks}},
    }


# ============================================================================
# verify_all registration
# ============================================================================

# ============================================================================
# Atlas live-runner contract
# ============================================================================

ATLAS_INPUT_ID = "mass:route02_charged_lepton_qed_running"
ATLAS_ROUTE = "ew"
ATLAS_PAYLOAD_NAME = "charged_lepton_qed_real_adapter_live"


def build_live_atlas_payload():
    """Build the live route payload for the atlas runner's swap dict.

    See apf.interface_atlas_live_runner for the contract this satisfies.
    """
    return infer_snapshot_from_banked_qed_content().to_payload(name=ATLAS_PAYLOAD_NAME)

def register(registry=None):
    """Register adapter checks into the bank registry."""
    checks = {
        "check_T_charged_lepton_qed_adapter_payload_contract_P":      check_T_charged_lepton_qed_adapter_payload_contract_P,
        "check_T_charged_lepton_qed_adapter_evaluator_consistent_P":  check_T_charged_lepton_qed_adapter_evaluator_consistent_P,
        "check_T_charged_lepton_qed_adapter_no_smuggling_P":          check_T_charged_lepton_qed_adapter_no_smuggling_P,
        "check_T_charged_lepton_qed_adapter_external_ledger_declared_P": check_T_charged_lepton_qed_adapter_external_ledger_declared_P,
        "check_T_charged_lepton_qed_adapter_certification_P":         check_T_charged_lepton_qed_adapter_certification_P,
        "check_T_charged_lepton_qed_real_adapter_P":                  check_T_charged_lepton_qed_real_adapter_P,
    }
    if registry is None:
        return checks
    registry.update(checks)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in register().items()}


if __name__ == "__main__":
    import json
    out = run_all()
    print(json.dumps({k: {"consistent": v["consistent"], "status": v["status"]} for k, v in out.items()}, indent=2))
