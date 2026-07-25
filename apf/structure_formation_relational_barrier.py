"""structure_formation_relational_barrier.py -- self-contained bank port of the
SFRS-v2 cyclic-co-requirement GRAPH THEOREM.

WHAT IS BANKED (and ONLY this). A precise, exact combinatorial theorem about
relational folds. A fold is a set of distinctions; a distinction may co-require
other distinctions (a distinction is admissible only if its relata are present
-- a compatibility / feasibility fact, never a cost). Building the fold by
"serial single-commitments" means adding one distinction at a time so that
every intermediate configuration is relata-closed. The banked result is:

    An admissible whole fold is UNREACHABLE by monotone serial single-
    commitments IFF its requirement digraph has a directed cycle (among
    distinct distinctions). A cyclically co-requiring fold has no admissible
    proper partial, so no order of single commits crosses it; the ONLY earned
    consequent is that a single-event JOINT COMMIT of >= 2 distinctions
    occurred. A non-cyclic (record / chain) fold IS serially reachable -- the
    separation is real, not vacuous.

    The barrier is RENT-FREE: cost is purely additive (eps*|S|), with no state-
    rent and no dangling / joint cost term. The barrier lives entirely in
    ADMISSIBILITY (relata-closure), never in the ledger. This respects, and is
    anchored on, the banked rent-exclusion theorem T_ledger_rent_excluded
    (check_T_ledger_rent_excluded, operational_completeness.py): the ledger
    bills TRANSITIONS, never a STATE for being held, so the barrier cannot be,
    and is not, a derived cost. Reversibility does not lift it.

WHAT IS NOT BANKED (named premise / fenced reading). The quantum-occupancy
reading is NOT established here and is NOT banked; it is a NAMED PREMISE.
"Serial impossible" earns only "a joint commit occurred"; it does NOT earn
"coherent hold", "slack", "A2 selection among co-held alternatives", or
"quantum occupancy" / OCC_Q. Those steps live in words, not in this model, and
are barred from citation (see MAY_NOT_CITE). The operative premise is CYCLIC
co-requirement -- a substantive structural stipulation, NOT "relationality"
(an acyclic relational chain assembles serially). Why fundamental folds would
be cyclically co-requiring rather than well-founded is an open problem.

GRADE: [P_structural] (epistemic="P_structural") on every banked check.
ppc=False (physical_premises_certified=False) on every check; non-exporting;
stdlib-only self-contained (fractions / itertools / collections / random).

Ruling of record (AUDIT_FINDINGS_SFRS, 2026-07-24): "We did NOT derive quantum
occupancy from built structure ... the earned consequent is 'a joint commit
occurred.'" Stage-2 reduction of the IFF: 0/6000 mismatches.
"""

from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass
from fractions import Fraction as Fr
from itertools import combinations, product
from typing import Dict, FrozenSet, Set, Tuple

FAMILY = "structure.cyclic_corequirement_serial_barrier"

# Claims this module's results do NOT support and that MUST NOT be cited from
# any of its checks. The quantum-occupancy reading is a named premise, not a
# banked result; the earned consequent is only "a joint commit occurred".
MAY_NOT_CITE: Tuple[str, ...] = (
    "structure => quantum occupancy",
    "occupancy is derived (from A1 or from built structure)",
    "structure => OCC_Q",
    "the joint commit is a coherent hold / slack "
    "(hold dynamics are NOT modeled; the earned consequent is only "
    "'a joint commit occurred')",
    "the joint seat selects among co-held alternatives / A2 selection "
    "(selection-forcing is open, not modeled)",
    "'structure formation requires slack' as a derived claim "
    "(only 'a joint commit is required for assembly' is earned)",
    "relationality is the operative premise "
    "(the operative premise is CYCLIC co-requirement, a substantive structural "
    "stipulation; an acyclic relational chain assembles serially)",
    "the cost-derivation route is walled / v2 escapes the joint-ness "
    "(v2 RELOCATES joint-ness from cost to a non-separable feasibility "
    "condition; it does not eliminate it)",
)

Config = FrozenSet[int]


@dataclass(frozen=True)
class RelationalModel:
    """A fold as a web of relational distinctions.

    ground   : the distinctions.
    requires : d -> the distinctions d co-requires (d is admissible only if they
               are present). A compatibility / feasibility fact, NOT a cost.
    eps      : MD floor billed per committed distinction (cost is ADDITIVE only).
    budget   : admissible cost ceiling (A1 endpoint gating).
    """
    ground: FrozenSet[int]
    requires: Dict[int, FrozenSet[int]]
    eps: Fr
    budget: Fr

    def relata_closed(self, S: Config) -> bool:
        """Every present distinction has its relata present (the relational
        admissibility constraint -- a feasibility fact, not a cost)."""
        return all(self.requires.get(d, frozenset()) <= S for d in S)

    def cost(self, S: Config) -> Fr:
        # PURELY additive: no dangling term, no joint term. Rent-free.
        return self.eps * len(S)

    def admissible(self, S: Config) -> bool:
        return self.relata_closed(S) and self.cost(S) <= self.budget


def serial_reachable(target: Config, m: RelationalModel,
                     allow_remove: bool = False) -> bool:
    """Gapless regime (single commits). Every visited configuration must be
    ADMISSIBLE (relata-closed and within budget). Returns whether the target
    fold is reachable from the empty seat by monotone single additions (and,
    if allow_remove, single removals)."""
    start: Config = frozenset()
    if not m.admissible(start):
        return target == start
    seen: Set[Config] = {start}
    q = deque([start])
    while q:
        S = q.popleft()
        if S == target:
            return True
        nbrs = [frozenset(S | {i}) for i in m.ground if i not in S]
        if allow_remove:
            nbrs += [frozenset(S - {i}) for i in S]
        for T in nbrs:
            if T not in seen and m.admissible(T):
                seen.add(T)
                q.append(T)
    return target in seen


def hold_reachable(target: Config, m: RelationalModel) -> bool:
    """A single-event joint commit seats the whole relata-closed fold in one
    step. Admissible iff relata-closed and within budget.

    NOTE (fence): serial-impossibility together with hold_reachable earns ONLY
    the consequent "a >= 2-distinction joint commit occurred". It does NOT earn
    coherent hold / slack / selection / quantum occupancy (see MAY_NOT_CITE)."""
    return m.admissible(target)


def _has_requirement_cycle(ground: FrozenSet[int],
                           requires: Dict[int, FrozenSet[int]]) -> bool:
    """Directed-cycle detection on the requirement digraph (edges d -> r for
    r in requires[d]), among DISTINCT distinctions. Self-requirements (d -> d)
    are stripped: relata-closure checks the config AFTER d is added, so a self-
    requirement is vacuously satisfiable and never strands a distinction from a
    distinct relatum. Requirements outside the ground are ignored. Iterative
    three-colour DFS."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {d: WHITE for d in ground}
    for root in ground:
        if color[root] != WHITE:
            continue
        stack = [(root, iter(sorted(requires.get(root, frozenset()))))]
        color[root] = GRAY
        while stack:
            u, it = stack[-1]
            advanced = False
            for v in it:
                if v == u or v not in color:
                    continue
                if color[v] == GRAY:
                    return True
                if color[v] == WHITE:
                    color[v] = GRAY
                    stack.append((v, iter(sorted(requires.get(v, frozenset())))))
                    advanced = True
                    break
            if not advanced:
                color[u] = BLACK
                stack.pop()
    return False


# ---------------------------------------------------------------------------
# Canonical models
# ---------------------------------------------------------------------------

def cyclic_fold(base: int = 0, n: int = 3) -> Dict[int, FrozenSet[int]]:
    """A cycle d_base -> d_base+1 -> ... -> d_base (each requires the next).
    Only relata-closed subsets: the empty set and the whole cycle."""
    ds = [base + k for k in range(n)]
    return {ds[k]: frozenset({ds[(k + 1) % n]}) for k in range(n)}


def _frustrated_cyclic_model() -> RelationalModel:
    """One cyclic fold {0,1,2}; each distinction co-requires the next around the
    cycle. Cost additive eps*|S|; budget admits the whole fold (3*1.25 <= 4)."""
    return RelationalModel(
        ground=frozenset({0, 1, 2}),
        requires=cyclic_fold(0, 3),
        eps=Fr(5, 4),
        budget=Fr(4),
    )


def _record_control_model() -> RelationalModel:
    """Separation control: STANDALONE distinctions (no co-requirement). Every
    subset is relata-closed, so a gapless world builds it serially (records)."""
    return RelationalModel(
        ground=frozenset({0, 1, 2}),
        requires={0: frozenset(), 1: frozenset(), 2: frozenset()},
        eps=Fr(5, 4),
        budget=Fr(4),
    )


def _chain_control_model() -> RelationalModel:
    """Separation control: an open chain 0->1->2 (2 standalone). Acyclic, so the
    prefixes {2},{1,2},{0,1,2} are relata-closed and it is serially reachable."""
    return RelationalModel(
        ground=frozenset({0, 1, 2}),
        requires={0: frozenset({1}), 1: frozenset({2}), 2: frozenset()},
        eps=Fr(5, 4),
        budget=Fr(4),
    )


def relata_closed_subsets(m: RelationalModel):
    out = []
    g = sorted(m.ground)
    for k in range(len(g) + 1):
        for c in combinations(g, k):
            S = frozenset(c)
            if m.relata_closed(S):
                out.append(S)
    return out


# ---------------------------------------------------------------------------
# Model batteries for the IFF theorem
# ---------------------------------------------------------------------------

def _all_requirement_models(n: int):
    """All requirement digraphs on n distinctions with requires[d] a subset of
    the OTHER distinctions (a relational distinction co-requires others, never
    itself). Budget non-binding (whole fold exactly fits), so reachability is
    governed purely by relata-closure, not cost."""
    ground = frozenset(range(n))
    eps = Fr(5, 4)
    budget = eps * n
    others = {d: [x for x in range(n) if x != d] for d in range(n)}
    per_node = []
    for d in range(n):
        subs = [frozenset(c)
                for k in range(len(others[d]) + 1)
                for c in combinations(others[d], k)]
        per_node.append(subs)
    for combo in product(*per_node):
        yield RelationalModel(ground, {d: combo[d] for d in range(n)}, eps, budget)


def _random_requirement_model(n: int, rng: random.Random) -> RelationalModel:
    """A random requirement digraph on n distinctions (no self-requirement),
    budget non-binding."""
    eps = Fr(5, 4)
    req = {}
    for d in range(n):
        others = [x for x in range(n) if x != d]
        k = rng.randint(0, len(others))
        req[d] = frozenset(rng.sample(others, k))
    return RelationalModel(frozenset(range(n)), req, eps, eps * n)


# ---------------------------------------------------------------------------
# Banked checks -- ONLY the cyclic-co-requirement graph theorem. [P_structural]
# ---------------------------------------------------------------------------

def check_L_cyclic_corequirement_blocks_serial_assembly():
    """[P_structural] The canonical 3-cycle fold {0,1,2} (each distinction co-
    requires the next) has ONLY the empty set and the whole fold relata-closed,
    so it has no admissible proper partial. Monotone serial single-commit
    assembly is therefore impossible (BFS from the empty seat cannot take a
    first step). The ONLY earned consequent is that the built whole is reached
    by a single-event JOINT COMMIT of >= 2 distinctions. Acyclic controls (a
    standalone-record fold and an open chain) ARE serially reachable, so the
    separation is real, not vacuous.

    FENCE: 'serial impossible' earns 'a joint commit occurred' and NOTHING
    MORE -- no coherent hold, no slack, no A2 selection, no quantum occupancy
    (see MAY_NOT_CITE)."""
    m = _frustrated_cyclic_model()
    whole = m.ground
    closed = [tuple(sorted(s)) for s in relata_closed_subsets(m)]
    no_proper_partial = (closed == [(), tuple(sorted(whole))])
    serial = serial_reachable(whole, m)
    joint = hold_reachable(whole, m)
    has_cycle = _has_requirement_cycle(m.ground, m.requires)

    rec = _record_control_model()
    chain = _chain_control_model()
    rec_serial = serial_reachable(rec.ground, rec)
    chain_serial = serial_reachable(chain.ground, chain)
    rec_acyclic = not _has_requirement_cycle(rec.ground, rec.requires)
    chain_acyclic = not _has_requirement_cycle(chain.ground, chain.requires)

    passed = (no_proper_partial and serial is False and joint is True
              and has_cycle is True
              and rec_serial is True and rec_acyclic is True
              and chain_serial is True and chain_acyclic is True)
    return {
        "passed": passed, "family": FAMILY, "epistemic": "P_structural",
        "physical_premises_certified": False,
        "relata_closed_subsets": closed,
        "no_admissible_proper_partial": no_proper_partial,
        "serial_single_commit_reachable": serial,
        "reached_only_by_joint_commit": (serial is False and joint is True),
        "requirement_digraph_has_cycle": has_cycle,
        "record_control_serially_reachable": rec_serial,
        "chain_control_serially_reachable": chain_serial,
        "earned_consequent":
            "a single-event joint commit of >=2 distinctions occurred",
        "cites": "T_ledger_rent_excluded (banked rent-exclusion anchor)",
        "may_not_cite": list(MAY_NOT_CITE),
    }


def check_L_serial_unreachable_iff_requirement_cycle():
    """[P_structural] THE GRAPH THEOREM. Over a deterministic battery -- ALL
    requirement digraphs on 3 and 4 distinctions (no self-requirement) plus a
    seeded random battery of 6000 digraphs on 4..7 distinctions -- the whole
    fold is UNREACHABLE by monotone serial single-commitments IFF its
    requirement digraph has a directed cycle (among distinct distinctions).
    Two independent algorithms are cross-checked: BFS serial reachability (the
    model) vs three-colour DFS cycle detection (the ground truth). Zero
    mismatches. Budget is held non-binding (the whole fold fits), so the
    barrier is purely the cycle, not cost. Both arms are witnessed (cyclic-and-
    unreachable and acyclic-and-reachable both occur).

    FENCE: the earned consequent of unreachability is only 'a joint commit
    occurred' (see MAY_NOT_CITE)."""
    rng = random.Random(20260724)
    tested = 0
    mismatches = 0
    cyclic_unreachable = 0
    acyclic_reachable = 0

    def _tally(m):
        nonlocal tested, mismatches, cyclic_unreachable, acyclic_reachable
        tested += 1
        serial = serial_reachable(m.ground, m)
        cyclic = _has_requirement_cycle(m.ground, m.requires)
        if serial == (not cyclic):
            if cyclic and serial is False:
                cyclic_unreachable += 1
            if (not cyclic) and serial is True:
                acyclic_reachable += 1
        else:
            mismatches += 1

    for m in _all_requirement_models(3):
        _tally(m)
    for m in _all_requirement_models(4):
        _tally(m)
    for _ in range(6000):
        n = rng.choice((4, 5, 6, 7))
        _tally(_random_requirement_model(n, rng))

    passed = (mismatches == 0 and tested >= 6000
              and cyclic_unreachable > 0 and acyclic_reachable > 0)
    return {
        "passed": passed, "family": FAMILY, "epistemic": "P_structural",
        "physical_premises_certified": False,
        "models_tested": tested,
        "iff_mismatches": mismatches,
        "cyclic_and_serially_unreachable": cyclic_unreachable,
        "acyclic_and_serially_reachable": acyclic_reachable,
        "theorem": "serial-unreachable(whole) IFF requirement digraph has a "
                   "directed cycle among distinct distinctions",
        "earned_consequent":
            "unreachable => a joint commit of >=2 distinctions occurred",
        "may_not_cite": list(MAY_NOT_CITE),
    }


def check_L_barrier_is_rent_free():
    """[P_structural] RENT-EXCLUSION. The cost is purely additive: cost(S) =
    eps*|S| for every subset, and any two configurations of equal size cost the
    same (no completeness / state rent). The barrier therefore lives entirely
    in ADMISSIBILITY (relata-closure), never in a dangling or joint cost term,
    and is invariant to the budget: raising the budget by a factor 10^9 leaves
    the cyclic whole serially unreachable. This is anchored on the banked
    rent-exclusion theorem T_ledger_rent_excluded -- the ledger bills
    transitions, not a state held -- so the barrier is rent-free and cannot be
    a derived cost."""
    m = _frustrated_cyclic_model()
    g = sorted(m.ground)
    additive = all(m.cost(frozenset(c)) == m.eps * len(c)
                   for k in range(len(g) + 1) for c in combinations(g, k))
    by_size: Dict[int, set] = {}
    for k in range(len(g) + 1):
        for c in combinations(g, k):
            by_size.setdefault(k, set()).add(m.cost(frozenset(c)))
    no_completeness_rent = all(len(v) == 1 for v in by_size.values())
    fat = RelationalModel(m.ground, m.requires, m.eps, m.eps * 10 ** 9)
    still_blocked = serial_reachable(fat.ground, fat) is False
    passed = additive and no_completeness_rent and still_blocked
    return {
        "passed": passed, "family": FAMILY, "epistemic": "P_structural",
        "physical_premises_certified": False,
        "cost_additive_in_size_only": additive,
        "no_completeness_rent": no_completeness_rent,
        "barrier_invariant_to_budget_1e9": still_blocked,
        "rent_exclusion_respected": additive and no_completeness_rent,
        "cites": "T_ledger_rent_excluded (banked rent-exclusion anchor)",
        "may_not_cite": list(MAY_NOT_CITE),
    }


def check_L_barrier_survives_reversibility():
    """[P_structural] REVERSIBILITY DOES NOT LIFT IT. Even when single-commit
    moves may be UNDONE (single removals as well as additions), the cyclic
    whole {0,1,2} remains serially unreachable: from the empty seat no
    admissible neighbour exists in either direction, so no reversible walk
    crosses the barrier. The obstruction is genuine impossibility -- a joint
    commit is required -- not an ordering / undo artifact. The acyclic record
    control stays reachable under reversible moves, so the control is live."""
    m = _frustrated_cyclic_model()
    whole = m.ground
    fwd = serial_reachable(whole, m, allow_remove=False)
    rev = serial_reachable(whole, m, allow_remove=True)
    rec = _record_control_model()
    rec_rev = serial_reachable(rec.ground, rec, allow_remove=True)
    passed = (fwd is False and rev is False and rec_rev is True)
    return {
        "passed": passed, "family": FAMILY, "epistemic": "P_structural",
        "physical_premises_certified": False,
        "serial_reachable_forward": fwd,
        "serial_reachable_with_reversibility": rev,
        "record_control_reachable_with_reversibility": rec_rev,
        "verdict":
            "reversibility does not make the cyclic whole serially reachable",
        "earned_consequent":
            "a joint commit of >=2 distinctions is still required",
        "may_not_cite": list(MAY_NOT_CITE),
    }


# ---------------------------------------------------------------------------
# Mutation battery (reported by run_all; NOT bank-registered)
# ---------------------------------------------------------------------------

def run_mutations():
    base = _frustrated_cyclic_model()
    whole = base.ground
    r = {}
    r["M1_baseline_cyclic_serial_blocked"] = (serial_reachable(whole, base) is False)
    drop = RelationalModel(base.ground,
                           {0: frozenset(), 1: frozenset(), 2: frozenset()},
                           base.eps, base.budget)
    r["M2_drop_corequirements_serial_ok"] = (serial_reachable(whole, drop) is True)
    r["M3_open_cycle_to_chain_serial_ok"] = (
        serial_reachable(whole, _chain_control_model()) is True)
    tight = RelationalModel(base.ground, base.requires, base.eps, Fr(2))
    r["M4_budget_below_fold_joint_blocked"] = (hold_reachable(whole, tight) is False)
    r["all_caught"] = all(r.values())
    return r


_CHECKS = {
    "L_cyclic_corequirement_blocks_serial_assembly":
        check_L_cyclic_corequirement_blocks_serial_assembly,
    "L_serial_unreachable_iff_requirement_cycle":
        check_L_serial_unreachable_iff_requirement_cycle,
    "L_barrier_is_rent_free":
        check_L_barrier_is_rent_free,
    "L_barrier_survives_reversibility":
        check_L_barrier_survives_reversibility,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all(verbose=True):
    out = {}
    for name, fn in _CHECKS.items():
        rr = fn()
        out[name] = rr
        if verbose:
            print(("PASS" if rr["passed"] else "FAIL"), name,
                  "[" + rr["epistemic"] + "]")
    muts = run_mutations()
    out["mutations"] = muts
    if verbose:
        n = sum(1 for k in muts if k.startswith("M"))
        print(("PASS" if muts["all_caught"] else "FAIL"),
              "mutation_battery ({} named)".format(n))
        npass = sum(1 for k, v in out.items() if k != "mutations" and v["passed"])
        print("== {} / {} checks pass; mutations all caught: {}".format(
            npass, len(_CHECKS), muts["all_caught"]))
    return out


if __name__ == "__main__":
    res = run_all()
    ok = all(v["passed"] for k, v in res.items() if k != "mutations") \
        and res["mutations"]["all_caught"]
    raise SystemExit(0 if ok else 1)
