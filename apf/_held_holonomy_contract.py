"""Private H1-H7 dependency-cycle certificate for :mod:`apf.held_holonomy`."""
from __future__ import annotations
from ._held_holonomy_common import *
DEPENDENCY_CONTRACT: Dict[str, Tuple[str, ...]] = {
    "H1": (
        "REVERSIBLE_HELD_CLOSURE", "TWO_SIDED_CONGRUENCE",
        "REVERSAL_IS_INVERSE",
    ),
    "H2": ("H1", "RECOMBINATION_WITNESS"),
    "H3": ("H1", "CONNECTED_REGIME_R", "CONTINUITY"),
    "H4": (
        "QUADRATIC_LEDGER",
        "Q2_LEDGER_ADJOINT",
        "REVERSAL_IS_INVERSE",
    ),
    "H5": (
        "ELEMENTARY_BIPOLAR_SPLIT",
        "FIRST_ORDER_LOCAL_COMPLETENESS",
        "MINIMUM_COMPLETE_CARRIER",
    ),
    "H6": (
        "H2", "H3", "H4", "H5", "FAITHFUL_ACTION",
        "EFFECTIVE_IMAGE_LIE_SUBGROUP",
    ),
    "H7": (
        "H6", "JET_FUNCTORIALITY", "ORIENTATION_SYNCHRONIZATION",
        "CONTINUOUS_ORIENTATION_TRANSPORT",
        "CLOSED_WORLD_RECORD_COMPLETENESS",
    ),
    "CENTRAL_COMPLEX_TYPE": (
        "H7", "GENERATOR_COMPLETENESS", "FINITE_REAL_CSTAR_CLASSIFICATION",
    ),
}


def _complete_graph(graph: Mapping[str, Sequence[str]]) -> Dict[str, Tuple[str, ...]]:
    complete = {node: tuple(deps) for node, deps in graph.items()}
    for deps in graph.values():
        for dep in deps:
            complete.setdefault(dep, ())
    return complete


def _find_cycle(graph: Mapping[str, Sequence[str]]) -> Optional[Tuple[str, ...]]:
    complete = _complete_graph(graph)
    visiting: List[str] = []
    visited: FrozenSet[str] = frozenset()
    visited_mutable: set = set()

    def dfs(node: str) -> Optional[Tuple[str, ...]]:
        if node in visiting:
            start = visiting.index(node)
            return tuple(visiting[start:] + [node])
        if node in visited_mutable:
            return None
        visiting.append(node)
        for dep in complete[node]:
            cycle = dfs(dep)
            if cycle is not None:
                return cycle
        visiting.pop()
        visited_mutable.add(node)
        return None

    for node in complete:
        cycle = dfs(node)
        if cycle is not None:
            return cycle
    _ = visited  # keep the function's immutable-type contract explicit for 3.8.
    return None


def _depends_on(graph: Mapping[str, Sequence[str]], start: str, target: str) -> bool:
    complete = _complete_graph(graph)
    seen = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        for dep in complete.get(node, ()):
            if dep == target:
                return True
            stack.append(dep)
    return False


def held_holonomy_dependency_contract_impl() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    cycle = _find_cycle(DEPENDENCY_CONTRACT)
    ck(cycle is None, "canonical Held-holonomy dependency graph must be acyclic")
    ck(_depends_on(DEPENDENCY_CONTRACT, "H6", "H4"),
       "H6 must consume the independently established H4 isometry")
    ck(_depends_on(DEPENDENCY_CONTRACT, "H4", "QUADRATIC_LEDGER"),
       "H4 must declare the quadratic ledger input")
    ck(not _depends_on(DEPENDENCY_CONTRACT, "QUADRATIC_LEDGER", "H6"),
       "the quadratic ledger must not depend on the circle theorem")
    ck(not _depends_on(DEPENDENCY_CONTRACT, "Q2_LEDGER_ADJOINT", "H6"),
       "the Q2 adjoint must not be reconstructed from the Q4 circle")

    mutated = dict(DEPENDENCY_CONTRACT)
    mutated["QUADRATIC_LEDGER"] = ("H6",)
    mutated_cycle = _find_cycle(mutated)
    ck(mutated_cycle is not None,
       "cycle mutation QL<-H6 must be rejected")

    # A second mutation catches local/global centrality collapse.
    premature = dict(DEPENDENCY_CONTRACT)
    premature["CENTRAL_COMPLEX_TYPE"] = ("H6", "FINITE_REAL_CSTAR_CLASSIFICATION")
    ck(not _depends_on(premature, "CENTRAL_COMPLEX_TYPE", "H7"),
       "premature mutation really removes naturality/generator completeness")
    ck(_depends_on(DEPENDENCY_CONTRACT, "CENTRAL_COMPLEX_TYPE", "H7"),
       "canonical centrality must pass through H7")
    ck(_depends_on(DEPENDENCY_CONTRACT, "H6", "EFFECTIVE_IMAGE_LIE_SUBGROUP"),
       "H6 must declare the finite-dimensional Lie-image classification gate")
    ck(not _depends_on(DEPENDENCY_CONTRACT, "H7", "GENERATOR_COMPLETENESS"),
       "H7 naturality must not silently contain generator completeness")
    ck(_depends_on(DEPENDENCY_CONTRACT, "CENTRAL_COMPLEX_TYPE",
                   "GENERATOR_COMPLETENESS"),
       "central complex type must name generator completeness")
    ck(not _depends_on(DEPENDENCY_CONTRACT, "H6", "GENERATOR_COMPLETENESS"),
       "the local circle H6 must not silently contain the global generator premise")
    ck(_depends_on(DEPENDENCY_CONTRACT, "H1", "REVERSAL_IS_INVERSE"),
       "the H1 group claim must declare reversal-is-inverse: reversal "
       "admission alone yields only a monoid")
    ck(not _depends_on(DEPENDENCY_CONTRACT, "H2", "FAITHFUL_ACTION"),
       "H2 is an operational-quotient claim; effectiveness is gated at H6, "
       "not smuggled into the recombination witness")
    ck(_depends_on(DEPENDENCY_CONTRACT, "H6", "FAITHFUL_ACTION"),
       "effectiveness must be consumed exactly at H6")

    return _result(
        "T_held_holonomy_dependency_contract",
        "P_structural_instrument",
        ("The machine-readable H1-H7 graph is acyclic.  H6 consumes H4; H4 "
         "consumes the independently established quadratic ledger and Q2 adjoint. "
         "The mutation QUADRATIC_LEDGER<-H6 creates a detected cycle.  Central "
         "complex type is separately gated by H7 naturality, generator "
         "completeness, and the finite real C*-classification, so the local "
         "quarter-turn is not silently globalized."),
        [
            "T_held_relative_loop_group",
            "T_held_recombination_nontriviality",
            "T_held_connected_subgroup_so2",
            "T_reversible_ledger_isometry",
            "T_bipolar_first_jet_rank_two",
            "T_held_circle_quarter_turn",
            "T_held_jet_naturality",
            "T_central_complex_block_exclusion",
            "T_SAT_countermodel_is_bypassed_not_refuted",
        ],
        {
            "dependency_contract": {k: list(v) for k, v in DEPENDENCY_CONTRACT.items()},
            "canonical_cycle": cycle,
            "positivity_cycle_mutation_detected": mutated_cycle is not None,
            "positivity_cycle_mutation": list(mutated_cycle) if mutated_cycle else None,
            "centrality_requires_H7": True,
            "centrality_requires_generator_completeness": True,
            "H6_requires_Lie_image": True,
            "H1_requires_reversal_inverse": True,
            "H2_is_operational_scope": True,
            "SAT_load_bearing": False,
        },
        fails,
        premises=PHYSICAL_PREMISES,
        negative_controls=(
            "QUADRATIC_LEDGER -> H6 cycle mutation",
            "premature CENTRAL_COMPLEX_TYPE -> H6 mutation",
        ),
        cross_refs=(
            "Paper 5 Q1-Q5 gate discipline",
            "Paper 33 certificate/provenance discipline",
            "Paper 44 finite/continuum seam",
        ),
    )


