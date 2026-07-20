"""Held relative-loop holonomy -- exact finite certificates and scope guards.

This is the executable companion to the occupied Held-holonomy theorem in
Paper 5.  It certifies exact finite mathematics and the dependency contract;
it does not certify that the named physical premises obtain.

The canonical isometry route is the typed Q2 identity
``represented reversal = ledger adjoint = inverse``.  SAT / a physical defect
retract is retired as a load-bearing route, but its identity/exchange
countermodel remains valid and is retained as a negative control.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Callable, Dict, Mapping, Optional

from ._held_holonomy_common import (
    FAMILY,
    PAPER_TARGETS,
    PHYSICAL_PREMISES,
    FinitePath,
    HolonomyCertificate,
    PathClass,
)
from ._held_holonomy_contract import (
    DEPENDENCY_CONTRACT,
    held_holonomy_dependency_contract_impl,
)
from ._held_holonomy_groups import (
    held_connected_subgroup_so2_impl,
    held_recombination_nontriviality_impl,
    held_relative_loop_group_impl,
)
from ._held_holonomy_linear import (
    bipolar_first_jet_rank_two_impl,
    reversible_ledger_isometry_impl,
)
from ._held_holonomy_naturality import (
    held_circle_quarter_turn_impl,
    held_jet_naturality_impl,
)
from ._held_holonomy_blocks import (
    central_complex_block_exclusion_impl,
    sat_countermodel_bypassed_not_refuted_impl,
)


def check_T_held_relative_loop_group() -> Dict[str, object]:
    return held_relative_loop_group_impl()


def check_T_held_recombination_nontriviality() -> Dict[str, object]:
    return held_recombination_nontriviality_impl()


def check_T_held_connected_subgroup_so2() -> Dict[str, object]:
    return held_connected_subgroup_so2_impl()


def check_T_reversible_ledger_isometry() -> Dict[str, object]:
    return reversible_ledger_isometry_impl()


def check_T_bipolar_first_jet_rank_two() -> Dict[str, object]:
    return bipolar_first_jet_rank_two_impl()


def check_T_held_circle_quarter_turn() -> Dict[str, object]:
    return held_circle_quarter_turn_impl()


def check_T_held_jet_naturality() -> Dict[str, object]:
    return held_jet_naturality_impl()


def check_T_central_complex_block_exclusion() -> Dict[str, object]:
    return central_complex_block_exclusion_impl()


def check_T_SAT_countermodel_is_bypassed_not_refuted() -> Dict[str, object]:
    return sat_countermodel_bypassed_not_refuted_impl()


def check_T_held_holonomy_dependency_contract() -> Dict[str, object]:
    return held_holonomy_dependency_contract_impl()


_CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_held_relative_loop_group": check_T_held_relative_loop_group,
    "T_held_recombination_nontriviality": check_T_held_recombination_nontriviality,
    "T_held_connected_subgroup_so2": check_T_held_connected_subgroup_so2,
    "T_reversible_ledger_isometry": check_T_reversible_ledger_isometry,
    "T_bipolar_first_jet_rank_two": check_T_bipolar_first_jet_rank_two,
    "T_held_circle_quarter_turn": check_T_held_circle_quarter_turn,
    "T_held_jet_naturality": check_T_held_jet_naturality,
    "T_central_complex_block_exclusion": check_T_central_complex_block_exclusion,
    "T_SAT_countermodel_is_bypassed_not_refuted": check_T_SAT_countermodel_is_bypassed_not_refuted,
    "T_held_holonomy_dependency_contract": check_T_held_holonomy_dependency_contract,
}


def register(registry: Dict[str, object]) -> Dict[str, object]:
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in _CHECKS.items()}


def build_certificate(
    results: Optional[Mapping[str, Mapping[str, object]]] = None,
) -> HolonomyCertificate:
    rs = dict(results) if results is not None else run_all()

    def passed(name: str) -> bool:
        return bool(rs[name]["passed"])

    circle_schema = all((
        passed("T_held_recombination_nontriviality"),
        passed("T_held_connected_subgroup_so2"),
        passed("T_reversible_ledger_isometry"),
        passed("T_bipolar_first_jet_rank_two"),
        passed("T_held_circle_quarter_turn"),
    ))
    return HolonomyCertificate(
        group_axioms=passed("T_held_relative_loop_group"),
        nontrivial=passed("T_held_recombination_nontriviality"),
        connected_model=passed("T_held_connected_subgroup_so2"),
        isometric_action=passed("T_reversible_ledger_isometry"),
        rank_two=passed("T_bipolar_first_jet_rank_two"),
        full_so2_image=circle_schema,
        quarter_turn_square_minus_identity=passed("T_held_circle_quarter_turn"),
        naturality=passed("T_held_jet_naturality"),
        central_complex_block_exclusion=passed("T_central_complex_block_exclusion"),
        sat_bypassed_not_refuted=passed("T_SAT_countermodel_is_bypassed_not_refuted"),
        dependency_contract_acyclic=passed("T_held_holonomy_dependency_contract"),
        physical_premises_certified=False,
        scope="finite theorem schemas and negative controls; physical premises remain named",
        dependencies=tuple(PHYSICAL_PREMISES),
    )


IE_DECLARATIONS = (
    {
        "input_id": "quantum:held_holonomy_conditional_certificate",
        "axis": "ROUTE",
        "route": "held_relative_loop_holonomy",
        "expect_export": False,
        "payload": {
            "name": "held_holonomy_conditional_certificate",
            "closure_kind": "obstruction_named",
            "obstruction_class": "HELD_HOLONOMY_PHYSICAL_PREMISES_REQUIRED",
            "source_checks": list(_CHECKS),
            "open_obligations": list(PHYSICAL_PREMISES),
            "knockout_summary": (
                "The exact finite group, isometry, first-jet, circle, naturality, "
                "block-classification, SAT-disposition, and dependency-cycle "
                "certificates pass. The physical Held circle remains conditional "
                "on occupied coherence, connectedness, the Q2 adjoint, faithful "
                "first-order action, naturality, and generator completeness."
            ),
            "target_value_consumed": False,
        },
        "note": (
            "Conditional Paper-5 Q4 certificate. SAT is bypassed, not refuted; "
            "the quadratic ledger is upstream and protected by a cycle tripwire."
        ),
    },
)


if __name__ == "__main__":
    import json
    import sys

    results = run_all()
    certificate = build_certificate(results)
    payload = {
        "module": "held_holonomy_v1_0",
        "family": FAMILY,
        "check_count": len(results),
        "checks": {name: ("PASS" if result["passed"] else "FAIL")
                   for name, result in results.items()},
        "all_pass": all(bool(result["passed"]) for result in results.values()),
        "certificate": asdict(certificate),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    sys.exit(0 if payload["all_pass"] else 1)
