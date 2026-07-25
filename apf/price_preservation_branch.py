"""
price_preservation_branch.py -- The Zipper / Quantum-Interface lane, P15 (bank port)
================================================================================
Self-contained, scipy-free bank port of the Paper 5 Price-versus-Preservation
four-way Boolean branch classifier (source:
pool_p15_price_preservation_branch.py, APF_Quantum_Interface_EndToEnd intake;
clean-room re-implementation 2026-07-24). Exact arithmetic (fractions.Fraction);
no floats in the decision procedure, no scipy/numpy, no lane imports.

RESULT (machine-checked, honest). Given a COMPLETE finite Boolean defender class
for a queried behaviour -- each candidate carrying (i) whether it is a faithful
common Boolean / commuting defender at all [structural], (ii) how far it moves
the queried continuation profile [distance], (iii) what it charges the ledger
[cost] -- the class occupies EXACTLY ONE of four branches under a profile
tolerance tau and a capacity cap:

  ADMISSIBLE_BOOLEAN     a profile-preserving Boolean defender fits capacity.
                         -> No quantum structure required.
  CAPACITY_ONLY_FAILURE  a profile-preserving Boolean defender EXISTS but every
                         such defender is over budget (cost > cap).
                         -> No quantum structure required. PRICE-ONLY: enlarging
                            the ledger past the minimum preservation-feasible
                            cost restores ADMISSIBLE_BOOLEAN.
  PRESERVATION_IJC       structural defenders exist but every one moves the
                         queried profile beyond tolerance (distance > tau).
                         -> Non-Boolean bridge (quantum-admissible). Capacity is
                            INERT here: no ledger enlargement rescues it.
  STRUCTURAL_IJC         no faithful common Boolean defender exists at all.
                         -> Non-Boolean bridge (quantum-admissible).

THE LOAD-BEARING INSIGHT (with teeth). CAPACITY SHORTAGE ALONE DOES NOT IMPLY
QUANTUM STRUCTURE. CAPACITY_ONLY_FAILURE is exhibited concretely -- a behaviour
whose only profile-preserving Boolean defender is over budget -- and enlarging
the ledger flips it back to ADMISSIBLE_BOOLEAN. It is a Price fact, not a
Process-IJC fact. The contrast is exhibited too: for a PRESERVATION_IJC
behaviour every Boolean repair alters the queried profile, and NO capacity
enlargement changes the branch. Price rescues the first and cannot touch the
second. The active pattern's A2 price metadata is carried as diagnostics only;
the decision procedure does not read it.

GRADE: [P_structural_instrument] on every check. This is a DECISION PROCEDURE /
classification over a DECLARED finite defender class -- exact and total on that
class, with a real refutation surface on every leg (every branch responds to a
genuine mutation of the class, the tolerance, or the capacity; a dedicated
fail-control battery flips the branch four ways). It is NOT a proof over "all
possible defenders": the classification is exhaustive over the DECLARED class
only; an incomplete or empty class returns UNCERTIFIED, never a definite branch.
physical_premises_certified = False; non-exporting.

CONCORDANCES (cited, not re-derived):
  ijc_boolean_defender_bridge (.424, [P_math]): outside-polytope <=> no common
    Boolean / commuting defender (Fine facet). STRUCTURAL_IJC rides this banked
    equivalence; the module does not re-derive the polytope.
  fp4_process_defender ([P_structural] / [P_math]): the measurement-
    incompatibility gate = the banked IJC / Boolean-defender-infeasible
    condition. PRESERVATION_IJC and STRUCTURAL_IJC are the two ways that gate
    opens at the declared-interface level.
  T_IJC_dichotomy, T_no_IJC_no_noncommutativity, T_quantum_admissibility_condition:
    PLEC admits both branches; the branch (QAC) is empirical, not A1-forced.

MAY NOT BE CITED FROM THIS MODULE:
  'capacity shortage implies quantum' (FALSE -- CAPACITY_ONLY_FAILURE is the
    explicit counterexample, and refuting exactly this is the point of the module);
  any '[P]' on the branch / the four-way Price-vs-Preservation classification;
  'the classification is exhaustive over all possible defenders' (it is over the
    DECLARED finite defender class only; incomplete -> UNCERTIFIED);
  'the QAC is derived' / 'Held => quantum'.
"""

from collections import namedtuple
from fractions import Fraction as F
import random

FAMILY = "quantum.price_preservation_branch"

# ---- branch labels -------------------------------------------------------
ADMISSIBLE_BOOLEAN = "ADMISSIBLE_BOOLEAN"
CAPACITY_ONLY_FAILURE = "CAPACITY_ONLY_FAILURE"
PRESERVATION_IJC = "PRESERVATION_IJC"
STRUCTURAL_IJC = "STRUCTURAL_IJC"
UNCERTIFIED = "UNCERTIFIED"

BRANCHES = (ADMISSIBLE_BOOLEAN, CAPACITY_ONLY_FAILURE,
            PRESERVATION_IJC, STRUCTURAL_IJC)

# quantum-structure-required readout per branch (None = undetermined class).
# The load-bearing entry is CAPACITY_ONLY_FAILURE -> False: Price, not Process.
_QUANTUM_REQUIRED = {
    ADMISSIBLE_BOOLEAN: False,
    CAPACITY_ONLY_FAILURE: False,
    PRESERVATION_IJC: True,
    STRUCTURAL_IJC: True,
    UNCERTIFIED: None,
}

CROSS_REFS = [
    "T_ijc_boolean_defender_bridge",       # ijc_boolean_defender_bridge (.424)
    "L_fp4_structural_defender_exists",     # fp4_process_defender
    "L_fp4_minimal_clause_and_not_entailed",
    "T_IJC_dichotomy",
    "T_no_IJC_no_noncommutativity",
    "T_quantum_admissibility_condition",
]

MAY_NOT_CITE = [
    "capacity shortage implies quantum (FALSE -- CAPACITY_ONLY_FAILURE is the "
    "explicit counterexample; refuting this is the point of the module)",
    "any [P] on the branch / the four-way Price-vs-Preservation classification",
    "the classification is exhaustive over all possible defenders (it is over "
    "the DECLARED finite defender class only; incomplete -> UNCERTIFIED)",
    "the QAC is derived / Held => quantum",
]


# a candidate common Boolean defender for the queried behaviour:
#   structural : is it a faithful common Boolean / commuting defender at all?
#   distance   : how far it moves the queried continuation profile (>= 0)
#   cost       : what it charges the ledger (>= 0)
Candidate = namedtuple("Candidate", ("name", "structural", "distance", "cost"))


def cand(name, structural, distance, cost):
    d = F(distance)
    c = F(cost)
    if d < 0 or c < 0:
        raise ValueError("distance and cost must be nonnegative")
    return Candidate(name, bool(structural), d, c)


def classify(candidates, tolerance, capacity, complete=True, a2_score=0):
    """The decision procedure over a declared defender class.

    ``a2_score`` is accepted -- it is the active pattern's A2 price metadata --
    but is not read by the decision procedure (diagnostics only). An incomplete
    or empty declared class returns UNCERTIFIED, never a branch.

    The three filters nest by construction:
        admissible  subset  preservation  subset  structural,
    so the if/elif cascade returns exactly one branch."""
    if not complete or not candidates:
        return UNCERTIFIED
    tau = F(tolerance)
    cap = F(capacity)
    structural = [c for c in candidates if c.structural]
    preservation = [c for c in structural if c.distance <= tau]
    admissible = [c for c in preservation if c.cost <= cap]
    if admissible:
        return ADMISSIBLE_BOOLEAN
    if preservation:
        return CAPACITY_ONLY_FAILURE
    if structural:
        return PRESERVATION_IJC
    return STRUCTURAL_IJC


def branch_predicates(candidates, tolerance, capacity):
    """cross-check predicate (shares the nesting logic), written straight from
    the nesting admissible subset preservation subset structural rather than via
    the if/elif ordering of ``classify``. Certifies exclusivity/exhaustivity with
    teeth: if ``classify``'s cascade ordering were mutated it would disagree
    with these predicates on some class."""
    tau = F(tolerance)
    cap = F(capacity)
    S = any(c.structural for c in candidates)
    P = any(c.structural and c.distance <= tau for c in candidates)
    A = any(c.structural and c.distance <= tau and c.cost <= cap
            for c in candidates)
    return {
        ADMISSIBLE_BOOLEAN: A,
        CAPACITY_ONLY_FAILURE: P and not A,
        PRESERVATION_IJC: S and not P,
        STRUCTURAL_IJC: not S,
    }


def min_preservation_cost(candidates, tolerance):
    """The capacity threshold: the cheapest profile-preserving structural
    defender's cost, or None if no structural defender preserves the profile."""
    tau = F(tolerance)
    costs = [c.cost for c in candidates
             if c.structural and c.distance <= tau]
    return min(costs) if costs else None


def quantum_required(branch):
    return _QUANTUM_REQUIRED[branch]


# =====================================================================
# P15-A -- the four-way classifier is total and mutually exclusive
# =====================================================================

def check_T_price_preservation_branch_classification():
    """[P_structural_instrument]. The Price-vs-Preservation classifier is TOTAL
    and MUTUALLY EXCLUSIVE on every complete declared defender class: exactly one
    of the four branches fires and it agrees with the independent nesting
    predicates (admissible subset preservation subset structural). The four
    canonical scenarios land in their branches; an incomplete or empty class
    returns UNCERTIFIED (never a branch)."""
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        return cond

    # the four canonical scenarios land exactly (each branch computed)
    adm = classify([cand("D0", True, 0, 1)], tolerance=0, capacity=1)
    capf = classify([cand("D1", True, 0, 3)], tolerance=0, capacity=2)
    pre = classify([cand("D2", True, F(1, 4), 1)], tolerance=0, capacity=10)
    strc = classify([cand("bad", False, 0, 0)], tolerance=0, capacity=10)
    ck(adm == ADMISSIBLE_BOOLEAN, "canonical admissible -> ADMISSIBLE_BOOLEAN")
    ck(capf == CAPACITY_ONLY_FAILURE,
       "canonical capacity_only -> CAPACITY_ONLY_FAILURE")
    ck(pre == PRESERVATION_IJC, "canonical preservation -> PRESERVATION_IJC")
    ck(strc == STRUCTURAL_IJC, "canonical structural -> STRUCTURAL_IJC")

    # totality + exclusivity + agreement with the independent predicates over a
    # deterministic randomized battery of declared classes.
    rng = random.Random(20260724)
    classifier_agrees = True
    branch_hits = {b: 0 for b in BRANCHES}
    for _ in range(4000):
        n = rng.randint(1, 4)
        cs = [cand("c%d" % i, rng.random() < 0.6,
                   F(rng.randint(0, 4), 4), F(rng.randint(0, 6)))
              for i in range(n)]
        tol = F(rng.randint(0, 4), 4)
        capv = F(rng.randint(0, 6))
        preds = branch_predicates(cs, tol, capv)
        b = classify(cs, tol, capv)
        if not preds.get(b, False):
            classifier_agrees = False
        branch_hits[b] = branch_hits.get(b, 0) + 1
    ck(classifier_agrees,
       "classify agrees with the independent nesting predicates (battery)")
    ck(all(branch_hits[b] > 0 for b in BRANCHES),
       "all four branches exercised by the battery")

    # completeness gate: incomplete or empty class -> UNCERTIFIED, not a branch
    ck(classify([cand("D0", True, 0, 1)], 0, 1, complete=False) == UNCERTIFIED,
       "incomplete class -> UNCERTIFIED")
    ck(classify([], 0, 1) == UNCERTIFIED, "empty class -> UNCERTIFIED")

    passed = not fails
    return {
        "name": "T_price_preservation_branch_classification",
        "epistemic": "P_structural_instrument",
        "passed": passed,
        "tier": 4,
        "physical_premises_certified": False,
        "family": FAMILY,
        "key_result": (
            "the four-way Price-vs-Preservation classifier over a COMPLETE "
            "declared finite Boolean defender class is total and mutually "
            "exclusive: it agrees with the independent nesting predicates "
            "(admissible subset preservation subset structural) over a 4000-case "
            "battery hitting all four branches; incomplete/empty -> UNCERTIFIED. "
            "Classification over the DECLARED class, NOT over all possible "
            "defenders."
        ),
        "branches": list(BRANCHES),
        "canonical_scenarios_correct": (adm == ADMISSIBLE_BOOLEAN
                                        and capf == CAPACITY_ONLY_FAILURE
                                        and pre == PRESERVATION_IJC
                                        and strc == STRUCTURAL_IJC),
        "battery_branch_hits": branch_hits,
        "classifier_agrees_with_independent_predicates": classifier_agrees,
        "dependencies": [],
        "cross_refs": CROSS_REFS,
        "grade_gate": (
            "exact total decision procedure on the DECLARED finite class "
            "(instrument-class); NOT a proof over all possible defenders. "
            "Incomplete class -> UNCERTIFIED. No [P] on the classification."
        ),
        "may_not_cite": MAY_NOT_CITE,
        "fail_reasons": fails,
    }


# =====================================================================
# P15-B -- capacity shortage alone does NOT imply quantum (the teeth)
# =====================================================================

def check_T_capacity_shortage_not_quantum():
    """[P_structural_instrument]. THE load-bearing fact: capacity shortage alone
    does NOT imply quantum structure. A behaviour whose ONLY profile-preserving
    Boolean defender is over budget classifies as CAPACITY_ONLY_FAILURE -- No
    quantum -- and enlarging the ledger past the minimum preservation-feasible
    cost restores ADMISSIBLE_BOOLEAN. Price-only, never Process-IJC. A cheap
    defender that alters the profile is present but is NOT a preservation
    witness, so it cannot rescue the branch either."""
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        return cond

    # a pointed class: the ONLY profile-preserving defender (D_pre) is costly;
    # a cheap defender exists but ALTERS the queried profile (distance > tau).
    D_pre = cand("D_pre", True, 0, 5)          # preserves profile, cost 5
    D_cheap = cand("D_cheap", True, F(1, 2), 1)  # cheap but alters the profile
    cls = [D_pre, D_cheap]
    tau = F(0)

    thr = min_preservation_cost(cls, tau)
    ck(thr == F(5), "min preservation-feasible cost threshold = 5")

    # under budget: CAPACITY_ONLY_FAILURE, and NOT quantum
    b_under = classify(cls, tau, capacity=3)
    ck(b_under == CAPACITY_ONLY_FAILURE, "cap=3 < 5 -> CAPACITY_ONLY_FAILURE")
    ck(quantum_required(b_under) is False,
       "CAPACITY_ONLY_FAILURE requires NO quantum structure")

    # just below threshold still CAPACITY_ONLY (cheap altering defender ignored)
    ck(classify(cls, tau, capacity=4) == CAPACITY_ONLY_FAILURE,
       "cap=4 < 5 still CAPACITY_ONLY_FAILURE")

    # FAIL-CONTROL: enlarge the ledger to the threshold -> the branch FLIPS to
    # ADMISSIBLE_BOOLEAN. The classification genuinely responds; not hardcoded.
    b_restored = classify(cls, tau, capacity=5)
    ck(b_restored == ADMISSIBLE_BOOLEAN,
       "cap=5 >= threshold -> ADMISSIBLE_BOOLEAN (ledger enlargement restores it)")
    ck(quantum_required(b_restored) is False,
       "restored branch requires no quantum structure")
    branch_flips = (b_under != b_restored)
    ck(branch_flips, "the CAPACITY_ONLY -> ADMISSIBLE flip actually occurs")

    # the threshold is exactly the min preservation cost: below -> CAPACITY_ONLY,
    # at/above -> ADMISSIBLE (Price-only restoration is monotone in capacity).
    below = all(classify(cls, tau, k) == CAPACITY_ONLY_FAILURE
                for k in (F(0), F(1), F(4), F(9, 2)))
    atabove = all(classify(cls, tau, k) == ADMISSIBLE_BOOLEAN
                  for k in (F(5), F(6), F(100)))
    ck(below and atabove,
       "capacity threshold at min preservation cost 5: below CAPACITY_ONLY, "
       "at/above ADMISSIBLE")

    # the cheap-but-altering defender is NOT a valid preservation witness
    ck(min_preservation_cost([D_cheap], tau) is None,
       "the cheap profile-altering defender is not preservation-feasible")

    passed = not fails
    return {
        "name": "T_capacity_shortage_not_quantum",
        "epistemic": "P_structural_instrument",
        "passed": passed,
        "tier": 4,
        "physical_premises_certified": False,
        "family": FAMILY,
        "key_result": (
            "capacity shortage alone does NOT imply quantum structure: a class "
            "whose only profile-preserving Boolean defender costs 5 under "
            "capacity 3 is CAPACITY_ONLY_FAILURE (quantum_required False), and "
            "enlarging the ledger to the min preservation-feasible cost (5) "
            "flips it to ADMISSIBLE_BOOLEAN. Price-only, never Process-IJC; the "
            "cheap profile-altering defender is not a preservation witness."
        ),
        "min_preservation_cost": str(thr),
        "branch_under_budget": b_under,
        "branch_after_ledger_enlargement": b_restored,
        "capacity_only_requires_no_quantum": quantum_required(b_under) is False,
        "ledger_enlargement_restores_classicality": branch_flips,
        "dependencies": [],
        "cross_refs": CROSS_REFS,
        "grade_gate": (
            "exact instrument on the declared class; the CAPACITY_ONLY_FAILURE "
            "branch is Price, not Process -- do NOT cite 'capacity shortage "
            "implies quantum'."
        ),
        "may_not_cite": MAY_NOT_CITE,
        "fail_reasons": fails,
    }


# =====================================================================
# P15-C -- preservation failure is a genuine, price-irreducible bridge
# =====================================================================

def check_T_preservation_ijc_price_irreducible():
    """[P_structural_instrument]. The contrast to CAPACITY_ONLY_FAILURE. A
    PRESERVATION_IJC behaviour -- structural defenders exist but every one moves
    the queried profile beyond tolerance -- requires a non-Boolean bridge
    (quantum-admissible), and NO ledger enlargement changes the branch. Price
    rescues CAPACITY_ONLY_FAILURE but is INERT here. Loosening the tolerance to
    admit the profile change DOES flip it out of IJC, so the preservation
    distinction is real, not vacuous."""
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        return cond

    # every structural defender alters the profile (distance > tau = 0)
    cls = [cand("D_a", True, F(1, 4), 1), cand("D_b", True, F(1, 2), 1)]
    tau = F(0)
    b = classify(cls, tau, capacity=10)
    ck(b == PRESERVATION_IJC, "structural-but-altering class -> PRESERVATION_IJC")
    ck(quantum_required(b) is True,
       "PRESERVATION_IJC requires a non-Boolean bridge (quantum-admissible)")

    # capacity is INERT: no ledger enlargement (or shrink) moves the branch
    caps = (F(0), F(1), F(2), F(10), F(10 ** 6))
    capacity_inert = len({classify(cls, tau, k) for k in caps}) == 1
    ck(capacity_inert,
       "capacity inert for PRESERVATION_IJC (no ledger rescue)")
    ck(all(classify(cls, tau, k) == PRESERVATION_IJC for k in caps),
       "branch stays PRESERVATION_IJC across all capacities")

    # FAIL-CONTROL: loosen tolerance to admit the profile change -> flips OUT of
    # IJC (real distinction, not vacuous). At tau=1/2 both defenders preserve and
    # the cheaper one (cost 1) fits capacity -> ADMISSIBLE_BOOLEAN.
    b_loose = classify(cls, tolerance=F(1, 2), capacity=10)
    ck(b_loose == ADMISSIBLE_BOOLEAN,
       "tolerance >= distance flips PRESERVATION_IJC out to ADMISSIBLE_BOOLEAN")
    ck(b_loose != b, "the tolerance-driven branch flip actually occurs")

    # the sharp contrast: capacity flips CAPACITY_ONLY but is inert on this one
    cap_scn = [cand("D_pre", True, 0, 5)]
    cap_flips = (classify(cap_scn, 0, 3) != classify(cap_scn, 0, 5))
    pre_no_flip = (classify(cls, tau, 3) == classify(cls, tau, 5))
    ck(cap_flips and pre_no_flip,
       "capacity flips CAPACITY_ONLY but is inert on PRESERVATION_IJC")

    passed = not fails
    return {
        "name": "T_preservation_ijc_price_irreducible",
        "epistemic": "P_structural_instrument",
        "passed": passed,
        "tier": 4,
        "physical_premises_certified": False,
        "family": FAMILY,
        "key_result": (
            "PRESERVATION_IJC (structural defenders exist but all move the "
            "queried profile beyond tolerance) requires a non-Boolean bridge "
            "and is PRICE-IRREDUCIBLE: no ledger enlargement changes the branch "
            "(capacity inert across [0, 10^6]). Loosening the tolerance to admit "
            "the profile change flips it out to ADMISSIBLE_BOOLEAN, so the "
            "distinction is real, not vacuous. Sharp contrast: capacity flips "
            "CAPACITY_ONLY_FAILURE but cannot touch PRESERVATION_IJC."
        ),
        "branch": b,
        "preservation_ijc_requires_quantum": quantum_required(b) is True,
        "capacity_inert": capacity_inert,
        "tolerance_flip_branch": b_loose,
        "capacity_flips_price_case_but_not_preservation": (cap_flips
                                                           and pre_no_flip),
        "dependencies": [],
        "cross_refs": CROSS_REFS,
        "grade_gate": (
            "exact instrument on the declared class; PRESERVATION_IJC is the "
            "valid non-Boolean bridge, price-irreducible. No [P] on the branch."
        ),
        "may_not_cite": MAY_NOT_CITE,
        "fail_reasons": fails,
    }


# =====================================================================
# P15-D -- structural IJC + the four-way branch fail-control battery
# =====================================================================

def check_T_structural_ijc_and_branch_battery():
    """[P_structural_instrument]. The fourth branch and the explicit fail-control
    battery. STRUCTURAL_IJC: no faithful common Boolean defender exists at all --
    quantum-admissible, invariant under BOTH capacity and tolerance (neither
    price nor tolerance manufactures a defender the declared class does not
    contain). Then a battery of branch-flipping mutations, each of which MUST
    flip the branch to the named target -- proof that no leg is hardcoded and
    every branch is reachable and responsive."""
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        return cond

    # STRUCTURAL_IJC: no structural defender in the declared class
    cls = [cand("bad1", False, 0, 0), cand("bad2", False, F(1, 3), 2)]
    b = classify(cls, tolerance=0, capacity=10)
    ck(b == STRUCTURAL_IJC, "no faithful defender -> STRUCTURAL_IJC")
    ck(quantum_required(b) is True,
       "STRUCTURAL_IJC requires a non-Boolean bridge (quantum-admissible)")

    # invariant under capacity AND tolerance (nothing manufactures a defender)
    inert = {classify(cls, tolerance=t, capacity=k)
             for t in (F(0), F(1, 2), F(10)) for k in (F(0), F(3), F(10 ** 6))}
    ck(inert == {STRUCTURAL_IJC},
       "STRUCTURAL_IJC invariant under all tolerance/capacity")

    # FAIL-CONTROL BATTERY: each mutation flips the branch to the named target.
    base = [cand("D_pre", True, 0, 5), cand("D_cheap", True, F(1, 2), 1)]
    start = classify(base, 0, 3)   # CAPACITY_ONLY_FAILURE
    muts = {}
    # (a) enlarge the ledger -> ADMISSIBLE_BOOLEAN
    muts["cap_up_flips_to_admissible"] = (
        start == CAPACITY_ONLY_FAILURE
        and classify(base, 0, 5) == ADMISSIBLE_BOOLEAN)
    # (b) drop the preserving defender -> PRESERVATION_IJC (only altering left)
    muts["drop_preserver_flips_to_preservation_ijc"] = (
        classify([base[1]], 0, 3) == PRESERVATION_IJC)
    # (c) make every defender unfaithful -> STRUCTURAL_IJC
    muts["unfaithful_flips_to_structural_ijc"] = (
        classify([c._replace(structural=False) for c in base], 0, 3)
        == STRUCTURAL_IJC)
    # (d) loosen tolerance so the cheap altering defender preserves -> ADMISSIBLE
    muts["tolerance_up_flips_to_admissible"] = (
        classify(base, F(1, 2), 3) == ADMISSIBLE_BOOLEAN)
    # (e) drop completeness -> UNCERTIFIED (not a definite branch)
    muts["incomplete_flips_to_uncertified"] = (
        classify(base, 0, 3, complete=False) == UNCERTIFIED)
    for k, v in muts.items():
        ck(v, "fail-control flip: " + k)

    # every branch is actually reached by at least one control (no dead branch)
    reached = {
        classify(base, 0, 3),                                     # CAPACITY_ONLY
        classify(base, 0, 5),                                     # ADMISSIBLE
        classify([base[1]], 0, 3),                                # PRESERVATION
        classify([c._replace(structural=False) for c in base], 0, 3),  # STRUCT
    }
    ck(reached == set(BRANCHES),
       "all four branches reached by the fail-control battery")

    passed = not fails
    return {
        "name": "T_structural_ijc_and_branch_battery",
        "epistemic": "P_structural_instrument",
        "passed": passed,
        "tier": 4,
        "physical_premises_certified": False,
        "family": FAMILY,
        "key_result": (
            "STRUCTURAL_IJC (no faithful common Boolean defender in the declared "
            "class) requires a non-Boolean bridge and is invariant under both "
            "capacity and tolerance. The fail-control battery flips the branch "
            "four ways -- ledger-up -> ADMISSIBLE, drop-preserver -> "
            "PRESERVATION_IJC, unfaithful -> STRUCTURAL_IJC, tolerance-up -> "
            "ADMISSIBLE, incomplete -> UNCERTIFIED -- reaching all four branches; "
            "no classifier leg is hardcoded."
        ),
        "branch": b,
        "structural_ijc_requires_quantum": quantum_required(b) is True,
        "structural_ijc_invariant": inert == {STRUCTURAL_IJC},
        "fail_control_flips": muts,
        "all_four_branches_reached": reached == set(BRANCHES),
        "dependencies": [],
        "cross_refs": CROSS_REFS,
        "grade_gate": (
            "exact instrument on the declared class; the battery certifies the "
            "classifier responds to genuine mutations. No [P] on the branch."
        ),
        "may_not_cite": MAY_NOT_CITE,
        "fail_reasons": fails,
    }


_CHECKS = {
    "T_price_preservation_branch_classification":
        check_T_price_preservation_branch_classification,
    "T_capacity_shortage_not_quantum":
        check_T_capacity_shortage_not_quantum,
    "T_preservation_ijc_price_irreducible":
        check_T_preservation_ijc_price_irreducible,
    "T_structural_ijc_and_branch_battery":
        check_T_structural_ijc_and_branch_battery,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all(verbose=True):
    out = {}
    for name, fn in _CHECKS.items():
        r = fn()
        out[name] = r
        if verbose:
            print(("PASS" if r["passed"] else "FAIL"), name,
                  "[" + r["epistemic"] + "]")
            for fr in r["fail_reasons"]:
                print("   -", fr)
    if verbose:
        npass = sum(1 for r in out.values() if r["passed"])
        print("== %d / %d checks pass" % (npass, len(_CHECKS)))
    return out


if __name__ == "__main__":
    import sys
    res = run_all()
    sys.exit(0 if all(r["passed"] for r in res.values()) else 1)
