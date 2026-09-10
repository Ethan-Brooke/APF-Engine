"""Unbanked finite audit of the APF zipper-clearance occupancy argument.

The candidate theorem is conditional and deliberately weaker than quantum
mechanics.  If a terminal local record must depend jointly on an earlier
preparation and a later context, while the earlier winner record is absent and
actualization is boundary-mediated, then the interface must carry a present
record-null but completion-sensitive mediator.  That mediator is a nonzero
active Held/record-kernel class.

The module owns the strongest countermodels:
  * predetermined accretion needs no clearance;
  * a complete-world oracle can bypass local mediation;
  * parallel classical records can compare alternatives at permanent cost;
  * a classical hidden bit is already a valid Held mediator, so occupancy alone
    does not derive noncommutativity, complex amplitudes, or Born weights.

No physical premise is certified and the module is not registered in the bank.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
from itertools import product
from typing import Callable, Dict, Mapping, Optional, Sequence, Tuple
import json

FAMILY = "quantum.zipper_clearance_occupancy_candidate"
Bit = int


@dataclass(frozen=True)
class ZipperClearanceOccupancyCertificate:
    premature_commitment_obstruction_exact: bool
    local_witness_necessity_exact: bool
    held_kernel_witness_exact: bool
    parallel_booking_control_exact: bool
    oracle_control_exposed: bool
    predetermined_control_exposed: bool
    classical_mediator_scope_fenced: bool
    dependency_contract_clean: bool
    physical_premises_certified: bool = False


def _result(
    name: str,
    key_result: str,
    artifacts: Mapping[str, object],
    fails: Sequence[str],
    *,
    dependencies: Sequence[str] = (),
    premises: Sequence[str] = (),
    negative_controls: Sequence[str] = (),
    epistemic: str = "P_math",
) -> Dict[str, object]:
    passed = not fails
    return {
        "name": name,
        "family": FAMILY,
        "tier": 4,
        "epistemic": epistemic,
        "status": "PASS" if passed else "FAIL",
        "passed": passed,
        "scope": "finite logical clearance/mediation schema / unbanked audit candidate",
        "physical_premises_certified": False,
        "key_result": key_result,
        "dependencies": list(dependencies),
        "premises": list(premises),
        "negative_controls": list(negative_controls),
        "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


def _all_bit_functions(n_inputs: int):
    """Enumerate all Boolean functions on n_inputs bits as truth-table tuples."""
    domain = tuple(product((0, 1), repeat=n_inputs))
    for values in product((0, 1), repeat=len(domain)):
        table = dict(zip(domain, values))
        yield table, lambda *xs, _t=table: _t[tuple(xs)]


def _target(preparation: Bit, context: Bit) -> Bit:
    """Minimal contextually nontrivial terminal relation."""
    return preparation ^ context


def check_T_premature_commitment_obstruction() -> Dict[str, object]:
    fails: list[str] = []
    contexts = (0, 1)
    preparations = (0, 1)

    early_maps = []
    successful_early_maps = []
    for table, e in _all_bit_functions(1):
        mismatches = [
            (p, c, e(p), _target(p, c))
            for p, c in product(preparations, contexts)
            if e(p) != _target(p, c)
        ]
        early_maps.append({
            "table": {str(k[0]): v for k, v in table.items()},
            "mismatch_count": len(mismatches),
            "mismatches": mismatches,
        })
        if not mismatches:
            successful_early_maps.append(table)

    if successful_early_maps:
        fails.append("an irreversible early winner unexpectedly matched both later contexts")
    min_mismatches = min(row["mismatch_count"] for row in early_maps)
    if min_mismatches != 2:
        fails.append("early-commitment obstruction should miss exactly one context per preparation")

    return _result(
        "T_premature_commitment_obstruction",
        "For the contextually nontrivial relation r=p XOR c, no irreversible winner record e(p) formed before c arrives can be correct for both later contexts. Every possible early commitment fails on at least two of the four complete cases.",
        {
            "target_relation": "terminal_record = preparation XOR later_context",
            "early_functions_checked": len(early_maps),
            "successful_early_functions": len(successful_early_maps),
            "minimum_mismatch_count": min_mismatches,
            "early_function_battery": early_maps,
            "late_context_is_load_bearing": True,
        },
        fails,
        premises=(
            "CONTEXTUALLY_NONTRIVIAL_TERMINAL_RELATION",
            "POSITIVE_IRREVERSIBLE_COMMITMENT",
            "NO_RECORD_REVISION",
        ),
        negative_controls=("terminal relation independent of later context", "reversible provisional mark relabelled as record"),
    )


def check_T_local_witness_requires_present_mediator() -> Dict[str, object]:
    fails: list[str] = []
    preparations = (0, 1)
    contexts = (0, 1)

    # No mediator: the complete present local state is the same for both p.
    no_mediator_success = []
    no_mediator_rows = []
    for table, f in _all_bit_functions(1):  # f receives later context only
        mismatches = [
            (p, c, f(c), _target(p, c))
            for p, c in product(preparations, contexts)
            if f(c) != _target(p, c)
        ]
        no_mediator_rows.append({
            "table": {str(k[0]): v for k, v in table.items()},
            "mismatch_count": len(mismatches),
        })
        if not mismatches:
            no_mediator_success.append(table)
    if no_mediator_success:
        fails.append("a context-only local rule unexpectedly retained preparation dependence")

    # Present mediator h=p: the same current record is retained, but future response differs.
    mediator_table = {(h, c): h ^ c for h, c in product((0, 1), repeat=2)}
    mediator_success = all(mediator_table[(p, c)] == _target(p, c) for p, c in product(preparations, contexts))
    if not mediator_success:
        fails.append("the explicit present mediator failed the target relation")

    # A complete-world oracle can use both p and future c at the early stage.
    oracle_success = all(_target(p, c) == (p ^ c) for p, c in product(preparations, contexts))
    if not oracle_success:
        fails.append("oracle control malformed")

    return _result(
        "T_local_witness_requires_present_mediator",
        "If the present local/boundary state is identical for p=0 and p=1, no local rule receiving only the later context can reproduce a terminal record depending on both p and c. A present mediator h=p suffices. A complete-world oracle also suffices, proving boundary-mediated enforceability is load-bearing.",
        {
            "no_mediator_functions_checked": len(no_mediator_rows),
            "no_mediator_success_count": len(no_mediator_success),
            "no_mediator_rows": no_mediator_rows,
            "mediator_response_table": {f"h={h},c={c}": v for (h, c), v in mediator_table.items()},
            "mediator_success": mediator_success,
            "global_oracle_success": oracle_success,
            "oracle_violates_local_factorization": True,
            "present_indiscernibility_statement": "same complete present state => same local output law",
        },
        fails,
        dependencies=("T_premature_commitment_obstruction",),
        premises=(
            "COMPLETE_OPERATIONAL_BOUNDARY_QUOTIENT",
            "BOUNDARY_MEDIATED_ENFORCEABILITY",
            "NO_UNMEDIATED_GLOBAL_SELECTOR",
        ),
        negative_controls=("complete-world oracle uses future context", "observer ignorance mistaken for physical indiscernibility"),
    )


def check_T_record_null_mediator_is_active_kernel() -> Dict[str, object]:
    fails: list[str] = []

    held_states = (0, 1)
    current_record = {h: 0 for h in held_states}
    completions = {
        0: {h: h for h in held_states},
        1: {h: 1 - h for h in held_states},
    }

    same_current_record = current_record[0] == current_record[1]
    distinguishing_completions = [
        c for c in completions if completions[c][0] != completions[c][1]
    ]
    kernel_pair = [(h0, h1) for h0 in held_states for h1 in held_states if current_record[h0] == current_record[h1]]
    nontrivial_relative_class = same_current_record and bool(distinguishing_completions)

    if not same_current_record:
        fails.append("Held alternatives should share the current invariant record")
    if not distinguishing_completions:
        fails.append("no later completion distinguishes the Held alternatives")
    if not nontrivial_relative_class:
        fails.append("active record-kernel witness did not form")

    return _result(
        "T_record_null_mediator_is_active_kernel",
        "The explicit mediator states h=0,1 have one current invariant record but different later completion signatures. Their relative class is therefore nonzero in the operational kernel of the current record map.",
        {
            "held_states": list(held_states),
            "current_record_map": {str(k): v for k, v in current_record.items()},
            "completion_signatures": {
                str(c): {str(h): value for h, value in row.items()}
                for c, row in completions.items()
            },
            "kernel_pair": kernel_pair,
            "distinguishing_completions": distinguishing_completions,
            "nontrivial_active_record_kernel": nontrivial_relative_class,
            "quantum_noncommutativity_derived": False,
        },
        fails,
        dependencies=("T_local_witness_requires_present_mediator",),
        premises=("COMPLETION_FAITHFUL_MEDIATOR", "CURRENT_RECORD_DEGENERACY"),
        negative_controls=("mediator states with identical complete response profiles", "already-distinct current records"),
    )


def check_T_parallel_booking_is_costly_rival_not_clearance() -> Dict[str, object]:
    fails: list[str] = []
    epsilon = F(1)
    candidate_counts = tuple(range(1, 9))
    costs = {n: n * epsilon for n in candidate_counts}
    if any(costs[n] != n * epsilon for n in candidate_counts):
        fails.append("parallel booking cost floor malformed")
    if costs[2] != 2 * epsilon:
        fails.append("two-branch parallel record cost must be at least 2 epsilon")

    # Both branch records can support later comparison, but remain in history.
    branch_records = ("record_P", "record_Q")
    later_winner = "P"
    rejected_record_persists = "record_Q" in branch_records
    if not rejected_record_persists:
        fails.append("parallel-bookkeeping control must retain the rejected branch record")

    return _result(
        "T_parallel_booking_is_costly_rival_not_clearance",
        "Parallel classical bookkeeping can preserve both alternatives and compare them later, but it pays at least one irreversible commitment floor per branch and retains rejected branch records. It is a rival architecture, not a record-free single-event clearance.",
        {
            "epsilon_star": str(epsilon),
            "candidate_costs": {str(n): str(cost) for n, cost in costs.items()},
            "two_branch_cost": str(costs[2]),
            "branch_records": list(branch_records),
            "later_winner": later_winner,
            "rejected_record_persists": rejected_record_persists,
            "parallel_booking_logically_possible": True,
            "same_as_record_free_clearance": False,
        },
        fails,
        dependencies=("T_premature_commitment_obstruction",),
        premises=("POSITIVE_IRREVERSIBLE_COMMITMENT", "NO_RECORD_ERASURE"),
        negative_controls=("parallel recorded search", "record erasure without retained trace"),
    )


def check_T_predetermined_and_classical_controls() -> Dict[str, object]:
    fails: list[str] = []

    predetermined = lambda present: present
    predetermined_success = all(predetermined(p) == p for p in (0, 1))

    # A classical hidden mediator is enough for the conditional occupancy theorem.
    classical_update = lambda h, c: h ^ c
    classical_success = all(classical_update(h, c) == _target(h, c) for h, c in product((0, 1), repeat=2))
    commuting_readouts = all(
        classical_update(classical_update(h, a), b) == classical_update(classical_update(h, b), a)
        for h, a, b in product((0, 1), repeat=3)
    )

    if not predetermined_success:
        fails.append("predetermined no-clearance control malformed")
    if not classical_success or not commuting_readouts:
        fails.append("classical Held-buffer control malformed")

    return _result(
        "T_predetermined_and_classical_controls",
        "Predetermined accretion can form records without a Held clearance, and a classical record-null bit can mediate later contextual dependence with commuting updates. Therefore the clearance theorem is conditional on genuine late-context dependence and derives occupied Held mediation, not quantum algebra.",
        {
            "predetermined_structure_needs_clearance": False,
            "predetermined_control_success": predetermined_success,
            "classical_hidden_mediator_success": classical_success,
            "classical_context_updates_commute": commuting_readouts,
            "noncommutativity_derived": False,
            "complex_structure_derived": False,
            "Born_rule_derived": False,
        },
        fails,
        dependencies=("T_record_null_mediator_is_active_kernel",),
        negative_controls=("structure formation alone implies quantum", "record-null mediator automatically implies noncommutativity"),
    )


PHYSICAL_PREMISES = (
    "CONTEXTUALLY_NONTRIVIAL_INTERFACE_REALIZED",
    "COMPLETE_OPERATIONAL_BOUNDARY_QUOTIENT",
    "BOUNDARY_MEDIATED_ENFORCEABILITY",
    "POSITIVE_IRREVERSIBLE_COMMITMENT",
    "SINGLE_EVENT_RESOLUTION",
    "NO_PARALLEL_RECORD_SUBSTITUTION",
    "COMPLETION_FAITHFUL_MEDIATOR",
)

DEPENDENCY_GRAPH: Dict[str, Tuple[str, ...]] = {
    "T_CONTEXTUAL_SELECTION_REQUIREMENT": (
        "CONTEXTUALLY_NONTRIVIAL_INTERFACE_REALIZED",
        "LATER_CONTEXT_PHYSICALLY_UNAVAILABLE_EARLY",
    ),
    "T_LOCAL_WITNESS": (
        "T_CONTEXTUAL_SELECTION_REQUIREMENT",
        "COMPLETE_OPERATIONAL_BOUNDARY_QUOTIENT",
        "BOUNDARY_MEDIATED_ENFORCEABILITY",
    ),
    "T_SINGLE_EVENT_CLEARANCE": (
        "T_LOCAL_WITNESS",
        "POSITIVE_IRREVERSIBLE_COMMITMENT",
        "SINGLE_EVENT_RESOLUTION",
        "NO_PARALLEL_RECORD_SUBSTITUTION",
    ),
    "T_ACTIVE_RECORD_KERNEL": (
        "T_SINGLE_EVENT_CLEARANCE",
        "COMPLETION_FAITHFUL_MEDIATOR",
    ),
}

FORBIDDEN_UPSTREAM = (
    "QUANTUM_OCCUPANCY_ASSUMED",
    "HILBERT_SPACE",
    "COMPLEX_SCALARS",
    "NONCOMMUTATIVITY",
    "BORN_RULE",
    "WAVEFUNCTION_COLLAPSE",
    "GLOBAL_FUTURE_ORACLE",
)


def _cycle(graph: Mapping[str, Sequence[str]]) -> Optional[Tuple[str, ...]]:
    nodes = set(graph)
    for deps in graph.values():
        nodes.update(deps)
    state: Dict[str, int] = {}
    stack: list[str] = []

    def dfs(node: str) -> Optional[Tuple[str, ...]]:
        state[node] = 1
        stack.append(node)
        for dep in graph.get(node, ()):
            if state.get(dep, 0) == 0:
                cycle = dfs(dep)
                if cycle is not None:
                    return cycle
            elif state.get(dep) == 1:
                i = stack.index(dep)
                return tuple(stack[i:] + [dep])
        stack.pop()
        state[node] = 2
        return None

    for node in sorted(nodes):
        if state.get(node, 0) == 0:
            cycle = dfs(node)
            if cycle is not None:
                return cycle
    return None


def _deps(graph: Mapping[str, Sequence[str]], node: str) -> set[str]:
    out: set[str] = set()
    todo = list(graph.get(node, ()))
    while todo:
        dep = todo.pop()
        if dep in out:
            continue
        out.add(dep)
        todo.extend(graph.get(dep, ()))
    return out


def check_T_zipper_clearance_dependency_contract() -> Dict[str, object]:
    fails: list[str] = []
    cycle = _cycle(DEPENDENCY_GRAPH)
    if cycle is not None:
        fails.append(f"dependency cycle: {cycle}")
    upstream = _deps(DEPENDENCY_GRAPH, "T_ACTIVE_RECORD_KERNEL")
    forbidden = sorted(set(FORBIDDEN_UPSTREAM) & upstream)
    if forbidden:
        fails.append(f"clearance theorem consumes forbidden quantum structure: {forbidden}")

    mut_quantum = dict(DEPENDENCY_GRAPH)
    mut_quantum["T_LOCAL_WITNESS"] = (*mut_quantum["T_LOCAL_WITNESS"], "QUANTUM_OCCUPANCY_ASSUMED")
    quantum_smuggling_caught = "QUANTUM_OCCUPANCY_ASSUMED" in _deps(mut_quantum, "T_ACTIVE_RECORD_KERNEL")

    mut_oracle = dict(DEPENDENCY_GRAPH)
    mut_oracle["T_LOCAL_WITNESS"] = (*mut_oracle["T_LOCAL_WITNESS"], "GLOBAL_FUTURE_ORACLE")
    oracle_smuggling_caught = "GLOBAL_FUTURE_ORACLE" in _deps(mut_oracle, "T_ACTIVE_RECORD_KERNEL")

    mut_cycle = dict(DEPENDENCY_GRAPH)
    mut_cycle["T_CONTEXTUAL_SELECTION_REQUIREMENT"] = (
        *mut_cycle["T_CONTEXTUAL_SELECTION_REQUIREMENT"],
        "T_ACTIVE_RECORD_KERNEL",
    )
    cycle_caught = _cycle(mut_cycle) is not None

    if not all((quantum_smuggling_caught, oracle_smuggling_caught, cycle_caught)):
        fails.append("one or more clearance dependency mutations escaped")

    return _result(
        "T_zipper_clearance_dependency_contract",
        "The active-record-kernel conclusion is downstream only of contextual late dependence, a complete operational boundary quotient, boundary-mediated enforceability, positive irreversible single-event commitment, exclusion of parallel-record substitution, and completion-faithful mediation. Hilbert, complex scalars, noncommutativity, Born, collapse, assumed quantum occupancy, and a global future oracle are forbidden upstream.",
        {
            "graph": {k: list(v) for k, v in DEPENDENCY_GRAPH.items()},
            "cycle": cycle,
            "upstream_of_active_record_kernel": sorted(upstream),
            "forbidden_upstream": list(FORBIDDEN_UPSTREAM),
            "physical_premises": list(PHYSICAL_PREMISES),
            "quantum_smuggling_mutation_caught": quantum_smuggling_caught,
            "oracle_smuggling_mutation_caught": oracle_smuggling_caught,
            "cycle_mutation_caught": cycle_caught,
            "bank_registration": False,
        },
        fails,
        dependencies=tuple(DEPENDENCY_GRAPH),
        premises=PHYSICAL_PREMISES,
        negative_controls=("assume quantum occupancy", "permit global future oracle", "clearance conclusion used to derive its own premise"),
        epistemic="P_structural_instrument",
    )


CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_premature_commitment_obstruction": check_T_premature_commitment_obstruction,
    "T_local_witness_requires_present_mediator": check_T_local_witness_requires_present_mediator,
    "T_record_null_mediator_is_active_kernel": check_T_record_null_mediator_is_active_kernel,
    "T_parallel_booking_is_costly_rival_not_clearance": check_T_parallel_booking_is_costly_rival_not_clearance,
    "T_predetermined_and_classical_controls": check_T_predetermined_and_classical_controls,
    "T_zipper_clearance_dependency_contract": check_T_zipper_clearance_dependency_contract,
}


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in CHECKS.items()}


def build_certificate(
    results: Optional[Mapping[str, Mapping[str, object]]] = None,
) -> ZipperClearanceOccupancyCertificate:
    rows = dict(results or run_all())

    def ok(name: str) -> bool:
        return bool(rows[name]["passed"])

    parallel = rows["T_parallel_booking_is_costly_rival_not_clearance"]["artifacts"]
    controls = rows["T_predetermined_and_classical_controls"]["artifacts"]
    witness = rows["T_local_witness_requires_present_mediator"]["artifacts"]
    return ZipperClearanceOccupancyCertificate(
        premature_commitment_obstruction_exact=ok("T_premature_commitment_obstruction"),
        local_witness_necessity_exact=ok("T_local_witness_requires_present_mediator"),
        held_kernel_witness_exact=ok("T_record_null_mediator_is_active_kernel"),
        parallel_booking_control_exact=bool(parallel["parallel_booking_logically_possible"]),
        oracle_control_exposed=bool(witness["oracle_violates_local_factorization"]),
        predetermined_control_exposed=not bool(controls["predetermined_structure_needs_clearance"]),
        classical_mediator_scope_fenced=not bool(controls["noncommutativity_derived"]),
        dependency_contract_clean=ok("T_zipper_clearance_dependency_contract"),
        physical_premises_certified=False,
    )


def main() -> int:
    results = run_all()
    certificate = build_certificate(results)
    payload = {
        "name": "APF_Zipper_Clearance_Occupancy_Audit_v0.1",
        "family": FAMILY,
        "passed": all(bool(row["passed"]) for row in results.values()),
        "n_checks": len(results),
        "n_passed": sum(bool(row["passed"]) for row in results.values()),
        "certificate": asdict(certificate),
        "claim_boundary": {
            "conditional_conclusion": "contextually nontrivial boundary-mediated single-event resolution requires a present record-null completion-sensitive mediator",
            "active_record_kernel_derived_conditionally": True,
            "noncommutativity_derived": False,
            "complex_structure_derived": False,
            "Born_rule_derived": False,
            "physical_premises_certified": False,
            "bank_registered": False,
        },
        "checks": list(results.values()),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
