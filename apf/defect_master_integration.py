"""
APF Defect Master Integration v1

Status: [P_architecture]

This module binds the defect-calculus stack into a single architecture surface.

Integrated layers:
    1. Defect-Strata Calculus
    2. Defect Transition Dynamics
    3. Defect Composition Calculus
    4. Defect Variational Principle
    5. Defect Scale Flow
    6. Defect Obstruction Cohomology
    7. Defect Global Descent Kernel
    8. Defect Functorial Transport
    9. Defect Falsifier Gate Logic
    10. Defect Observable Signatures

Core doctrine:
    APF physics is represented architecturally as finite continuability
    organized by zero-defect strata, class transitions, composition laws,
    variational selection, scale flow, local-to-global descent, guarded
    transport, falsifier gates, and observable-signature templates.

This is architecture/math scaffolding only. It does not promote route-local
claims or assert empirical detection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Optional


STATUS = "[P_architecture]"
MARKER = "DEFECT_MASTER_INTEGRATION_PASS"


class DefectLayer(str, Enum):
    STRATA = "defect_strata"
    TRANSITION = "defect_transition"
    COMPOSITION = "defect_composition"
    VARIATIONAL = "defect_variational"
    SCALE_FLOW = "defect_scale_flow"
    OBSTRUCTION = "defect_obstruction"
    GLOBAL_DESCENT = "defect_global_descent"
    TRANSPORT = "defect_transport"
    FALSIFIER = "defect_falsifier"
    SIGNATURES = "defect_signatures"


@dataclass(frozen=True)
class LayerStatus:
    layer: DefectLayer
    module_name: str
    expected_marker: str
    installed: bool
    marker_matches: bool
    status: str = STATUS
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DefectStackReport:
    layers: tuple[LayerStatus, ...]
    all_installed: bool
    all_markers_match: bool
    status: str = STATUS
    marker: str = MARKER
    metadata: Mapping[str, Any] = field(default_factory=dict)


LAYER_MODULES = {
    DefectLayer.STRATA: ("apf.continuability_preservation_resolution", "DEFECT_STRATA_CALCULUS_PASS"),
    DefectLayer.TRANSITION: ("apf.defect_transition_dynamics", "DEFECT_TRANSITION_DYNAMICS_PASS"),
    DefectLayer.COMPOSITION: ("apf.defect_composition_calculus", "DEFECT_COMPOSITION_CALCULUS_PASS"),
    DefectLayer.VARIATIONAL: ("apf.defect_variational_principle", "DEFECT_VARIATIONAL_PRINCIPLE_PASS"),
    DefectLayer.SCALE_FLOW: ("apf.defect_scale_flow", "DEFECT_SCALE_FLOW_PASS"),
    DefectLayer.OBSTRUCTION: ("apf.defect_obstruction_cohomology", "DEFECT_OBSTRUCTION_COHOMOLOGY_PASS"),
    DefectLayer.GLOBAL_DESCENT: ("apf.defect_global_descent_kernel", "DEFECT_GLOBAL_DESCENT_KERNEL_PASS"),
    DefectLayer.TRANSPORT: ("apf.defect_functorial_transport", "DEFECT_FUNCTORIAL_TRANSPORT_PASS"),
    DefectLayer.FALSIFIER: ("apf.defect_falsifier_gate_logic", "DEFECT_FALSIFIER_GATE_LOGIC_PASS"),
    DefectLayer.SIGNATURES: ("apf.defect_observable_signatures", "DEFECT_OBSERVABLE_SIGNATURES_PASS"),
}


def _import_module(module_name: str):
    import importlib
    return importlib.import_module(module_name)


def layer_status(layer: DefectLayer) -> LayerStatus:
    module_name, expected_marker = LAYER_MODULES[layer]
    try:
        mod = _import_module(module_name)
        installed = True
        marker_value = mod.bank_marker() if hasattr(mod, "bank_marker") else getattr(mod, "MARKER", None)
        marker_matches = marker_value == expected_marker
        metadata = {"marker_value": marker_value}
    except Exception as exc:  # pragma: no cover
        installed = False
        marker_matches = False
        metadata = {"error": repr(exc)}
    return LayerStatus(
        layer=layer,
        module_name=module_name,
        expected_marker=expected_marker,
        installed=installed,
        marker_matches=marker_matches,
        metadata=metadata,
    )


def stack_report() -> DefectStackReport:
    layers = tuple(layer_status(layer) for layer in DefectLayer)
    return DefectStackReport(
        layers=layers,
        all_installed=all(x.installed for x in layers),
        all_markers_match=all(x.marker_matches for x in layers),
    )


def missing_layers(report: Optional[DefectStackReport] = None) -> tuple[DefectLayer, ...]:
    report = report or stack_report()
    return tuple(x.layer for x in report.layers if not x.installed)


def marker_mismatch_layers(report: Optional[DefectStackReport] = None) -> tuple[DefectLayer, ...]:
    report = report or stack_report()
    return tuple(x.layer for x in report.layers if x.installed and not x.marker_matches)


def defect_stack_ready(report: Optional[DefectStackReport] = None) -> bool:
    report = report or stack_report()
    return report.all_installed and report.all_markers_match


def architecture_guard() -> bool:
    """
    Master guard: this stack is architecture/math only.
    """
    return STATUS == "[P_architecture]"


def master_theorem_statement() -> str:
    return (
        "Defect Master Integration Theorem: In APF, finite continuability may be "
        "organized as a zero-defect architecture with strata, transitions, "
        "composition, variational selection, scale flow, obstruction/descent, "
        "functorial transport, falsifier gates, and observable-signature templates. "
        "The integrated stack is architecture-level and does not promote "
        "route-local physical claims or empirical detections."
    )


def layer_dependency_order() -> tuple[DefectLayer, ...]:
    return (
        DefectLayer.STRATA,
        DefectLayer.TRANSITION,
        DefectLayer.COMPOSITION,
        DefectLayer.VARIATIONAL,
        DefectLayer.SCALE_FLOW,
        DefectLayer.OBSTRUCTION,
        DefectLayer.GLOBAL_DESCENT,
        DefectLayer.TRANSPORT,
        DefectLayer.FALSIFIER,
        DefectLayer.SIGNATURES,
    )


def dependency_order_valid() -> bool:
    order = layer_dependency_order()
    return order[0] == DefectLayer.STRATA and order[-1] == DefectLayer.SIGNATURES and len(set(order)) == len(DefectLayer)


def integration_surface() -> Mapping[str, Any]:
    """
    Human/machine-readable integration declaration.
    """
    return {
        "name": "APF Defect Master Integration",
        "status": STATUS,
        "marker": MARKER,
        "doctrine": "architecture-only; no route-local promotion",
        "layers": tuple(layer.value for layer in layer_dependency_order()),
        "master_object": "finite continuability organized by zero-defect strata and guarded transport/descent",
    }


def bank_marker() -> str:
    return MARKER
