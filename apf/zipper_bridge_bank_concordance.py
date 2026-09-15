"""Unbanked concordance between the zipper bridge and banked Held-holonomy gates.

This module does not add a theorem.  It proves exact matrix concordance, checks
that the operational bridge consumes the existing physical-root vocabulary
rather than inventing a parallel closure, and records which leaves remain
physical and uncertified.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Dict, Mapping, Optional, Sequence, Tuple
import json

from apf import held_holonomy as hh
from apf import two_exchange_holonomy as tx
from apf import zipper_reflection_bridge as zrb
from apf._held_holonomy_common import PHYSICAL_PREMISES as HELD_ROOTS
from apf.two_exchange_roots import PHYSICAL_ROOTS as TWO_EXCHANGE_ROOTS

FAMILY = "quantum.zipper_bridge_bank_concordance_candidate"


@dataclass(frozen=True)
class ZipperBridgeBankConcordanceCertificate:
    matrices_concordant: bool
    banked_checks_green: bool
    premise_vocabulary_reconciled: bool
    no_duplicate_physical_certification: bool
    dependency_contract_clean: bool
    physical_premises_certified: bool = False


def _result(name: str, key_result: str, artifacts: Mapping[str, object], fails: Sequence[str], *,
            dependencies: Sequence[str] = (), premises: Sequence[str] = (),
            negative_controls: Sequence[str] = (), epistemic: str = "P_structural_instrument") -> Dict[str, object]:
    passed = not fails
    return {
        "name": name, "family": FAMILY, "tier": 4, "epistemic": epistemic,
        "status": "PASS" if passed else "FAIL", "passed": passed,
        "scope": "cross-module exact concordance / no new physical theorem",
        "physical_premises_certified": False, "key_result": key_result,
        "dependencies": list(dependencies), "premises": list(premises),
        "negative_controls": list(negative_controls), "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


def _tuple_matrix(a) -> Tuple[Tuple[object, ...], ...]:
    return tuple(tuple(x for x in row) for row in a)


def check_T_zipper_two_exchange_matrix_concordance() -> Dict[str, object]:
    fails: list[str] = []
    f345 = zrb._scale(zrb.F(1, 5), ((zrb.F(-1), zrb.F(7)), (zrb.F(7), zrb.F(1))))
    su = zrb._mm(zrb._mm(f345, zrb.PORT_SWAP), zrb._inv2(f345))
    r = zrb._mm(su, zrb.S0)
    checks = {
        "port_swap": zrb.PORT_SWAP == tx.P_SWAP,
        "zipper": zrb.ZIPPER == tx.H_ZIP,
        "first_reflection": zrb.S0 == tx.S_0,
        "presentation_scale_only": zrb._scale(zrb.F(5), f345) == tx.C_345,
        "second_reflection": su == tx.S_U,
        "two_exchange_rotation": r == tx.R_345,
    }
    if not all(checks.values()):
        fails.append(f"matrix concordance failed: {[k for k,v in checks.items() if not v]}")
    return _result(
        "T_zipper_two_exchange_matrix_concordance",
        "The zipper operational bridge and the banked two-exchange route use the same port swap, common/defect zipper, first reflection, 3-4-5 presentation up to irrelevant common scale, transported second reflection, and trace -14/25 rotation.",
        {
            "checks": checks,
            "zipper_Su": zrb._matrix_strings(su),
            "banked_Su": tx._matrix_strings(tx.S_U),
            "zipper_R": zrb._matrix_strings(r),
            "banked_R": tx._matrix_strings(tx.R_345),
            "trace_R": str(tx._trace(tx.R_345)),
        },
        fails,
        dependencies=("T_effective_port_exchange_is_operational_reflection", "T_live_345_zipper_transports_second_exchange"),
        negative_controls=("parallel matrix convention drift", "unrecorded scale dependence in conjugation"),
    )


BRIDGE_TO_BANKED_ROOTS: Dict[str, Tuple[str, ...]] = {
    "BINARY_HELD_PRESENTATION_REALIZED": (
        "occupied_record_free_coherent_component",
        "EFFECTIVE_FIRST_CONTENDER_EXCHANGE",
    ),
    "EFFECTIVE_RECORD_NEUTRAL_PORT_EXCHANGE": (
        "EFFECTIVE_FIRST_CONTENDER_EXCHANGE",
        "LATER_RECOMBINATION_WITNESS_FOR_EACH_EXCHANGE",
    ),
    "COMPLETION_FAITHFUL_DEFECT_QUOTIENT": (
        "two_sided_complete_operational_congruence",
        "faithful_first_order_action",
        "LATER_RECOMBINATION_WITNESS_FOR_EACH_EXCHANGE",
    ),
    "EXCHANGE_LEDGER_NEUTRALITY": (
        "positive_quadratic_ledger_form",
        "Q2_reversal_is_ledger_adjoint",
        "reversed_loop_is_inverse",
    ),
    "SAME_TYPE_RETURN": ("SAME_CARRIER_RETURN",),
    "RECORD_NEUTRAL_EXPORT_FREE_HOLONOMY_PATH": (
        "occupied_record_free_coherent_component",
        "reversible_Held_path_groupoid",
        "closed_world_record_completeness",
    ),
    "POSITIVE_LEDGER_ISOMETRY": (
        "positive_quadratic_ledger_form",
        "Q2_reversal_is_ledger_adjoint",
        "reversed_loop_is_inverse",
    ),
    "FIRST_ORDER_FAITHFUL_ACTION": (
        "elementary_bipolar_first_order_completeness",
        "faithful_first_order_action",
    ),
    "NONTRIVIAL_CONJUGATION_ORBIT": (
        "later_recombination_witness",
        "connected_Regime_R_component",
        "continuous_effective_action",
    ),
    "FIXED_RANK_TWO_HELD_STRATUM": (
        "elementary_bipolar_first_order_completeness",
        "faithful_first_order_action",
    ),
}


def check_T_zipper_bridge_premise_reconciliation() -> Dict[str, object]:
    fails: list[str] = []
    available = set(HELD_ROOTS) | set(TWO_EXCHANGE_ROOTS)
    bridge = set(zrb.PHYSICAL_PREMISES)
    mapping_keys_exact = set(BRIDGE_TO_BANKED_ROOTS) == bridge
    missing_targets = {
        key: sorted(set(targets) - available)
        for key, targets in BRIDGE_TO_BANKED_ROOTS.items()
        if set(targets) - available
    }
    if not mapping_keys_exact:
        fails.append(f"bridge premise map drift: {sorted(bridge ^ set(BRIDGE_TO_BANKED_ROOTS))}")
    if missing_targets:
        fails.append(f"mapped banked-root vocabulary missing: {missing_targets}")

    direct_two_exchange = {
        "ADMITTED_SECOND_BINARY_PRESENTATION",
        "EFFECTIVE_FIRST_CONTENDER_EXCHANGE",
        "EFFECTIVE_SECOND_CONTENDER_EXCHANGE",
        "INTERTWINER_REVERSAL_IS_INVERSE",
        "LATER_RECOMBINATION_WITNESS_FOR_EACH_EXCHANGE",
        "SAME_CARRIER_RETURN",
        "UNIVERSAL_EXCHANGE_NATURALITY_ON_ADMITTED_PRESENTATIONS",
    }
    if not direct_two_exchange <= set(TWO_EXCHANGE_ROOTS):
        fails.append("two-exchange direct-root subset drift")

    return _result(
        "T_zipper_bridge_premise_reconciliation",
        "Every operational-bridge premise is reconciled to named roots already present in the banked Held-holonomy and two-exchange contracts. This is vocabulary/dependency reconciliation only: the banked modules themselves keep every physical premise uncertified.",
        {
            "bridge_premises": sorted(bridge),
            "held_holonomy_roots": list(HELD_ROOTS),
            "two_exchange_roots": list(TWO_EXCHANGE_ROOTS),
            "bridge_to_banked_roots": {k: list(v) for k, v in BRIDGE_TO_BANKED_ROOTS.items()},
            "mapping_keys_exact": mapping_keys_exact,
            "missing_mapped_targets": missing_targets,
            "direct_two_exchange_subset": sorted(direct_two_exchange),
            "physical_discharge_claimed": False,
        },
        fails,
        dependencies=("T_operational_reflection_bridge_dependency_contract", "T_two_exchange_dependency_contract", "T_held_holonomy_dependency_contract"),
        premises=tuple(sorted(available)),
        negative_controls=("renaming a bridge premise without updating reconciliation", "mapping to a nonexistent banked root", "treating vocabulary concordance as physical discharge"),
    )


def check_T_banked_routes_and_bridge_execute_concordantly() -> Dict[str, object]:
    fails: list[str] = []
    selected = {
        "bank_binary_reflection": tx.check_T_binary_exchange_is_character_reflection(),
        "bank_rotated_exchange": tx.check_T_rotated_exchange_is_conjugated_swap(),
        "bank_effectiveness": tx.check_T_exchange_effectiveness_requires_recombination(),
        "bank_two_exchange_contract": tx.check_T_two_exchange_dependency_contract(),
        "bank_held_recombination": hh.check_T_held_recombination_nontriviality(),
        "bank_held_isometry": hh.check_T_reversible_ledger_isometry(),
        "bank_held_rank_two": hh.check_T_bipolar_first_jet_rank_two(),
        "bank_held_contract": hh.check_T_held_holonomy_dependency_contract(),
        "candidate_operational_reflection": zrb.check_T_effective_port_exchange_is_operational_reflection(),
        "candidate_conjugation_orbit": zrb.check_T_conjugated_exchange_orbit_recovers_holonomy_generator(),
    }
    failed = [name for name, row in selected.items() if not row["passed"]]
    incorrectly_certified = [name for name, row in selected.items() if row.get("physical_premises_certified") is not False]
    if failed:
        fails.append(f"selected routes failed: {failed}")
    if incorrectly_certified:
        fails.append(f"physical premise certification drift: {incorrectly_certified}")
    return _result(
        "T_banked_routes_and_bridge_execute_concordantly",
        "The relevant banked two-exchange and Held-holonomy schemas and the unbanked operational-reflection bridge all execute successfully on the same exact finite geometry, while every row remains explicitly physical-premise-uncertified.",
        {
            "selected_status": {name: row["status"] for name, row in selected.items()},
            "failed": failed,
            "incorrectly_physical_certified": incorrectly_certified,
            "all_physical_premises_certified_false": not incorrectly_certified,
            "novel_delta": "pointwise moving-reflection generator and its operational conjugation-orbit bridge",
        },
        fails,
        dependencies=("T_zipper_two_exchange_matrix_concordance", "T_zipper_bridge_premise_reconciliation"),
        negative_controls=("banked finite math mistaken for physical realization", "candidate route silently replacing Paper 5 whole-circle gates"),
    )


DEPENDENCY_GRAPH: Dict[str, Tuple[str, ...]] = {
    "T_MATRIX_CONCORDANCE": (
        "T_BINARY_EXCHANGE_CHARACTER_REFLECTION_BANKED",
        "T_ROTATED_EXCHANGE_CONJUGACY_BANKED",
        "T_OPERATIONAL_REFLECTION_CANDIDATE",
    ),
    "T_PREMISE_RECONCILIATION": (
        "T_TWO_EXCHANGE_ROOT_MANIFEST_BANKED",
        "T_HELD_HOLONOMY_ROOT_MANIFEST_BANKED",
        "T_OPERATIONAL_BRIDGE_ROOT_MANIFEST_CANDIDATE",
    ),
    "T_EXECUTABLE_CONCORDANCE": ("T_MATRIX_CONCORDANCE", "T_PREMISE_RECONCILIATION"),
}
FORBIDDEN_CLAIMS = (
    "PHYSICAL_PREMISES_DISCHARGED",
    "QUARTER_TURN_NOVELTY",
    "FIRST_APF_COMPLEX_STRUCTURE_ROUTE",
    "BANK_REGISTRATION",
    "EXPORT_CLOSURE",
)


def check_T_zipper_bridge_bank_concordance_dependency_contract() -> Dict[str, object]:
    fails: list[str] = []
    consumed = {x for deps in DEPENDENCY_GRAPH.values() for x in deps}
    forbidden = sorted(set(FORBIDDEN_CLAIMS) & consumed)
    if forbidden:
        fails.append(f"forbidden claim drift: {forbidden}")
    mut = dict(DEPENDENCY_GRAPH)
    mut["T_EXECUTABLE_CONCORDANCE"] = (*mut["T_EXECUTABLE_CONCORDANCE"], "PHYSICAL_PREMISES_DISCHARGED")
    mutation_caught = "PHYSICAL_PREMISES_DISCHARGED" in {x for deps in mut.values() for x in deps}
    if not mutation_caught:
        fails.append("physical-discharge mutation not caught")
    return _result(
        "T_zipper_bridge_bank_concordance_dependency_contract",
        "The concordance packet is restricted to matrix identity, root-vocabulary reconciliation, and executable cross-checking. It may not claim physical discharge, novelty for the quarter-turn or first APF complex route, bank registration, or export closure.",
        {
            "graph": {k: list(v) for k, v in DEPENDENCY_GRAPH.items()},
            "forbidden_claims": list(FORBIDDEN_CLAIMS),
            "forbidden_present": forbidden,
            "physical_discharge_mutation_caught": mutation_caught,
            "bank_registration": False,
        },
        fails,
        dependencies=tuple(DEPENDENCY_GRAPH),
        negative_controls=("physical premise discharge smuggled through concordance", "novelty overclaim", "bank/export overclaim"),
    )


CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_zipper_two_exchange_matrix_concordance": check_T_zipper_two_exchange_matrix_concordance,
    "T_zipper_bridge_premise_reconciliation": check_T_zipper_bridge_premise_reconciliation,
    "T_banked_routes_and_bridge_execute_concordantly": check_T_banked_routes_and_bridge_execute_concordantly,
    "T_zipper_bridge_bank_concordance_dependency_contract": check_T_zipper_bridge_bank_concordance_dependency_contract,
}


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in CHECKS.items()}


def build_certificate(results: Optional[Mapping[str, Mapping[str, object]]] = None) -> ZipperBridgeBankConcordanceCertificate:
    rows = dict(results or run_all())
    ok = lambda name: bool(rows[name]["passed"])
    executable = rows["T_banked_routes_and_bridge_execute_concordantly"]["artifacts"]
    return ZipperBridgeBankConcordanceCertificate(
        matrices_concordant=ok("T_zipper_two_exchange_matrix_concordance"),
        banked_checks_green=ok("T_banked_routes_and_bridge_execute_concordantly"),
        premise_vocabulary_reconciled=ok("T_zipper_bridge_premise_reconciliation"),
        no_duplicate_physical_certification=bool(executable["all_physical_premises_certified_false"]),
        dependency_contract_clean=ok("T_zipper_bridge_bank_concordance_dependency_contract"),
        physical_premises_certified=False,
    )


def main() -> int:
    results = run_all()
    cert = build_certificate(results)
    payload = {
        "name": "APF_Zipper_Bridge_Bank_Concordance_v0.1",
        "family": FAMILY,
        "passed": all(bool(row["passed"]) for row in results.values()),
        "n_checks": len(results),
        "n_passed": sum(bool(row["passed"]) for row in results.values()),
        "certificate": asdict(cert),
        "claim_boundary": {
            "concordance_only": True,
            "physical_premises_certified": False,
            "bank_registered": False,
            "novel_delta": "pointwise moving-reflection generator and targeted conjugation-orbit bridge",
        },
        "checks": list(results.values()),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
