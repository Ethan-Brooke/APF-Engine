#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
symmetry_cost_floor.py

APF bank module -- registered in BANK_REGISTRY_MODULES since v24.3.437
(occupant-cost arc, the zero-lemma, +2). Self-contained: stdlib + fractions +
itertools only. No scipy / numpy / multiprocessing.Pool / apf imports. Exact
arithmetic throughout (Fraction, int).

CARRIER NOTE (2026-08-01). The cost priced here lives on a FINITE CARRIER: a
configuration over X = {0..n-1}, priced by the pairs it tells apart under its
orbit partition. It is not a functional on a represented algebra, and no
construction in the bank carries a value between the two carriers. Any route
reading a score off this cost owes that transfer a definition first. Two
independent lanes have now stopped at this same point -- the held
``atomic_equal_cost_frame`` module (whose own scope note observes that a
projective ray in M_n(C) is a different carrier from this orbit partition, and
that the type-transfer is undefined), and the readout-completeness burden of
the Paper 5 Technical Supplement Q3E remark. NOT established, and not implied
by anything here: that the sandwich construction cannot run on this cost. See
``apf/ledger_extension_degree.py`` for what the banked cost does and does not
determine about degree.

------------------------------------------------------------------------------
THESIS UNDER TEST
------------------------------------------------------------------------------
APF reading of "cost": cost = enforced distinctions. MD (the positive floor):
every enforced distinction costs >= eps* > 0, and costs do NOT cancel (there
are no negative distinctions). A "configuration" over a finite carrier
X = {0..n-1} is a structure of enforced distinctions -- which elements are told
apart. The symmetry group of a configuration is the set of permutations of X
that preserve its enforced-distinction structure; two elements related by a
symmetry are NOT told apart, so nothing is enforced between them.

Claim to test: the cost-floor (the zero of the ledger) is the maximally
symmetric configuration. A symmetry is an ABSENCE of distinction, so maximal
symmetry = minimal enforced distinction = minimal cost. Concretely the
distinguishability structure of a group G acting on X is its ORBIT PARTITION:
elements in one orbit are interchangeable (not distinguished); elements in
different orbits are told apart (a distinction is enforced). Bigger symmetry
=> coarser orbit partition => fewer distinctions => lower cost. The full
symmetric group S_n merges everything into one orbit => zero enforced
distinctions => the floor.

------------------------------------------------------------------------------
TWO CHECKS
------------------------------------------------------------------------------
 1. check_L_orbit_count_monotone_in_symmetry  [P_math]
        Pure combinatorics. For G <= H <= S_n, #orbits(H) <= #orbits(G).
        Computed by real union-find over the actual group action (points and
        ordered pairs), on explicit subgroup families of S_4 and S_5.

 2. check_L_cost_floor_at_maximal_symmetry    [P_structural]
        The MD-dependent identification. cost(config) = eps* x (#separated
        pairs). Given non-negativity, "max symmetry = floor" is elementary:
        S_n (one orbit) separates nothing, so its cost is 0 = the minimum of a
        set of non-negative costs. MD's positive floor is precisely what
        supplies that non-negativity. Fail-control (existential): there EXISTS
        an MD-violating cost assignment -- the sign-flip eps* < 0, or the
        {0,1}|{2,..} cancelling scheme -- under which S_n is not the minimum.
        The check requires such a witness to bite, so MD's positivity is not
        idle. It does NOT claim that any weakening of MD breaks the floor.

------------------------------------------------------------------------------
SCOPE FENCES (enforced in may_not_cite on BOTH checks)
------------------------------------------------------------------------------
 * This is SYMMETRY-AS-ABSENCE-OF-DISTINCTION: a configuration simply does not
   separate x and y; nothing is enforced between them. It is NOT
   symmetry-as-enforced-invariance / GAUGE symmetry (an actively-maintained
   redundancy), which COSTS. Nothing here licenses "all symmetry is free."
 * The lemma gives a RELATIVE charge (a cost DIFFERENCE along the subgroup
   lattice), not an absolute-zero metaphysics of cost.
 * The physics application (a preferred foliation / hidden order is a
   symmetry-breaking that orthodox QM does not pay for) is NOT established here;
   it is a separate downstream premise (enforcement-realism + the specific
   broken symmetry).
 * The QAC does NOT lift from this lemma alone. This is step 1 of the QAC-lift
   surface (zero-lemma (this) / enforcement-realism / origin-forcing);
   G-hold-exact is now constitutively free under A2-exact (Ethan's ruling
   2026-07-26).

------------------------------------------------------------------------------
HONEST SCOPE (owned in-module, not smuggled)
------------------------------------------------------------------------------
 * ONE-WAY only. The converse ("floor => maximal symmetry") is FALSE: the floor
   (cost 0) is achieved by EVERY transitive configuration (single orbit) --
   V_4, C_4, A_4, S_4 all sit at 0. S_n is the MAXIMAL floor-achiever, not the
   unique one. The check verifies "max symmetry => floor", not the biconditional.
 * "Breaking a symmetry always costs" is FALSE. Only breaks that SEPARATE a
   previously-merged pair (refine the orbit partition) cost. Internal breaks
   that preserve the partition (S_4 -> A_4, S_4 -> C_4, S_4 -> V_4) are FREE on
   the point-distinction ledger. Cost is a function of the orbit PARTITION, not
   of the group; the group -> cost map factors through the partition.
 * cost = eps* x (#separated pairs) is a modelling choice (that is why check 2
   is [P_structural], not [P_math]): any cost that is strictly monotone in the
   coarsening of the orbit partition would carry the same conclusion.
"""

from fractions import Fraction
from itertools import combinations

# ============================================================================
# Permutation / group utilities  (stdlib only, exact)
# ============================================================================

def identity(n):
    return tuple(range(n))


def compose(p, q):
    """(p o q)(i) = p[q[i]] : apply q first, then p."""
    return tuple(p[q[i]] for i in range(len(q)))


def inverse(p):
    inv = [0] * len(p)
    for i, pi in enumerate(p):
        inv[pi] = i
    return tuple(inv)


def sign(p):
    """Parity of a permutation: (-1)^(n - #cycles). +1 even, -1 odd."""
    n = len(p)
    seen = [False] * n
    cycles = 0
    for i in range(n):
        if not seen[i]:
            cycles += 1
            j = i
            while not seen[j]:
                seen[j] = True
                j = p[j]
    return 1 if (n - cycles) % 2 == 0 else -1


def generate_group(gens, n):
    """Closure of <gens> under composition. BFS via left-multiplication by
    the generators AND their inverses -- guaranteed to produce the full
    subgroup <gens> of S_n, for any generating set (including the empty set,
    which yields the trivial group {e})."""
    e = identity(n)
    mults = [tuple(g) for g in gens] + [inverse(tuple(g)) for g in gens]
    elems = {e}
    frontier = [e]
    while frontier:
        nxt = []
        for x in frontier:
            for g in mults:
                y = compose(g, x)
                if y not in elems:
                    elems.add(y)
                    nxt.append(y)
        frontier = nxt
    return frozenset(elems)


# ============================================================================
# Group action / orbit utilities  (real union-find, no hardcoded counts)
# ============================================================================

def _uf_orbits(elements, points, act):
    """Orbits of the given group elements acting on 'points' under act(g, x).
    Computed by union-find over the ACTUAL action -- nothing is hardcoded."""
    idx = {x: k for k, x in enumerate(points)}
    parent = list(range(len(points)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for g in elements:
        for x in points:
            union(idx[x], idx[act(g, x)])

    blocks = {}
    for x in points:
        blocks.setdefault(find(idx[x]), []).append(x)
    return sorted(sorted(b) for b in blocks.values())


def orbits_on_points(elements, n):
    return _uf_orbits(elements, list(range(n)), lambda g, x: g[x])


def orbits_on_ordered_pairs(elements, n):
    pts = [(i, j) for i in range(n) for j in range(n)]
    return _uf_orbits(elements, pts, lambda g, x: (g[x[0]], g[x[1]]))


def separated_unordered_pairs(elements, n):
    """The enforced distinctions of the configuration whose non-distinctions
    are the orbits of 'elements': the unordered pairs {i, j} that land in
    DIFFERENT orbits (i.e. the configuration tells them apart)."""
    orb = orbits_on_points(elements, n)
    label = {}
    for k, block in enumerate(orb):
        for x in block:
            label[x] = k
    return [(i, j) for i, j in combinations(range(n), 2) if label[i] != label[j]]


# ============================================================================
# Explicit subgroup families of S_4 and S_5
# ============================================================================

def _sn_gens(n):
    """A transposition + an n-cycle generate the full symmetric group S_n."""
    trans = list(range(n))
    trans[0], trans[1] = 1, 0
    ncyc = tuple(list(range(1, n)) + [0])
    return [tuple(trans), ncyc]


def _pack(name, desc, elems, n):
    orb = orbits_on_points(elems, n)
    return {
        "name": name,
        "desc": desc,
        "elems": elems,
        "n": n,
        "order": len(elems),
        "orbits": orb,
        "num_orbits": len(orb),
        "num_pair_orbits": len(orbits_on_ordered_pairs(elems, n)),
        "sep_pairs": separated_unordered_pairs(elems, n),
        "num_sep": len(separated_unordered_pairs(elems, n)),
    }


def build_family(n):
    """A lattice-rich family of subgroups of S_n (n in {4, 5}), spanning the
    trivial group, point-stabilizers / Young subgroups, cyclics, the
    alternating group, and the full symmetric group."""
    fam = []

    def add(name, desc, gens):
        fam.append(_pack(name, desc, generate_group(gens, n), n))

    if n == 4:
        add("E4", "trivial {e}", [])
        add("C2_01", "swap (0 1)", [(1, 0, 2, 3)])
        add("C2_23", "swap (2 3)", [(0, 1, 3, 2)])
        add("C3_012", "3-cycle (0 1 2)", [(1, 2, 0, 3)])
        add("Young_2+2", "S2xS2 on {0,1}|{2,3}", [(1, 0, 2, 3), (0, 1, 3, 2)])
        add("S3_fix3", "S3 on {0,1,2}, fix 3", [(1, 0, 2, 3), (0, 2, 1, 3)])
        add("V4", "Klein four (all double transpositions)",
            [(1, 0, 3, 2), (2, 3, 0, 1)])
        add("C4", "4-cycle (0 1 2 3)", [(1, 2, 3, 0)])
        S4 = generate_group(_sn_gens(4), 4)
        A4 = frozenset(p for p in S4 if sign(p) == 1)
        fam.append(_pack("A4", "alternating group", A4, 4))
        fam.append(_pack("S4", "symmetric group (max symmetry)", S4, 4))

    elif n == 5:
        add("E5", "trivial {e}", [])
        add("C2_01", "swap (0 1)", [(1, 0, 2, 3, 4)])
        add("Young_2+2+1", "S2xS2xS1 on {0,1}|{2,3}|{4}",
            [(1, 0, 2, 3, 4), (0, 1, 3, 2, 4)])
        add("Young_2+3", "S2xS3 on {0,1}|{2,3,4}",
            [(1, 0, 2, 3, 4), (0, 1, 3, 2, 4), (0, 1, 2, 4, 3)])
        add("C5", "5-cycle (0 1 2 3 4)", [(1, 2, 3, 4, 0)])
        add("S4_fix4", "S4 on {0,1,2,3}, fix 4",
            [(1, 0, 2, 3, 4), (1, 2, 3, 0, 4)])
        S5 = generate_group(_sn_gens(5), 5)
        A5 = frozenset(p for p in S5 if sign(p) == 1)
        fam.append(_pack("A5", "alternating group", A5, 5))
        fam.append(_pack("S5", "symmetric group (max symmetry)", S5, 5))

    else:
        raise ValueError("n must be 4 or 5")

    return fam


def inclusion_pairs(fam):
    """All PROPER inclusions G < H present in the family, detected by an actual
    subset test on the element sets (frozensets of permutation tuples)."""
    out = []
    for G in fam:
        for H in fam:
            if G["name"] != H["name"] and G["elems"] <= H["elems"]:
                out.append((G, H))
    return out


# ============================================================================
# Cost model  (MD positive floor vs. cancelling regime)
# ============================================================================

def _pair_weight(pair, mode):
    """Weight of an enforced distinction on the pair {i, j}.

    mode='positive'   : MD floor -- every distinction weighs +1 (no cancel).
    mode='cancelling' : MD dropped -- distinctions that straddle the
                        {0,1} | {2,..} split weigh -1 (a cancelling term).
    """
    i, j = pair
    if mode == "positive":
        return Fraction(1)
    if mode == "cancelling":
        straddle = (i < 2) != (j < 2)
        return Fraction(-1) if straddle else Fraction(1)
    raise ValueError(mode)


def config_cost(group, eps_star, mode):
    """cost = eps* x sum of distinction weights over the SEPARATED pairs.
    Under the positive floor this is eps* x (#separated pairs)."""
    return eps_star * sum((_pair_weight(p, mode) for p in group["sep_pairs"]),
                          Fraction(0))


# ============================================================================
# Shared fence text
# ============================================================================

_MAY_NOT_CITE_COMMON = [
    "NOT gauge symmetry. This is symmetry-as-absence-of-distinction (a "
    "configuration does not separate x and y; nothing is enforced between "
    "them). An actively-maintained redundancy (enforced gauge invariance) "
    "COSTS. Do not cite as 'all symmetry is free' or 'gauge symmetry is free.'",
    "RELATIVE charge only. The lemma yields cost DIFFERENCES along the "
    "subgroup lattice, not an absolute-zero metaphysics of cost.",
    "Physics NOT established here. 'A preferred foliation / hidden order is an "
    "unpaid symmetry-breaking that orthodox QM does not charge for' is a "
    "separate downstream premise (enforcement-realism + a specific broken "
    "symmetry), not licensed by this lemma.",
    "QAC does NOT lift from this lemma. This is step 1 of the QAC-lift surface (zero-lemma / "
    "enforcement-realism / origin-forcing); G-hold-exact is now constitutively free under A2-exact (Ethan's ruling 2026-07-26); the quantum branch "
    "is not selected here.",
]

_CROSS_REFS = [
    "MD (positive cost floor: each enforced distinction costs >= eps* > 0, "
    "costs do not cancel)",
    "A1 (finite enforcement capacity)",
    "L_epsilon_star (the positive floor eps*)",
    "T_sep / enforced-distinction structure",
    "QAC-lift surface: zero-lemma (this) -> enforcement-realism -> "
    "origin-forcing (G-hold-exact is now constitutively free under A2-exact, Ethan's ruling 2026-07-26; cf. T_hold_cost_dominance_split)",
    # Occupant-cost arc: the breaks that DO cost (partition-refining / order-
    # refining) and the rent/occupant ledger that prices them.
    "order_refining_break",
    "rent_exclusion_gate",
    "occupant_cost_selection",
    "T_ledger_rent_excluded",
]


# ============================================================================
# CHECK 1 -- orbit count is monotone in symmetry   [P_math]
# ============================================================================

def check_L_orbit_count_monotone_in_symmetry():
    """[P_math] For G <= H <= S_n acting on a finite carrier X, the orbit
    partition of H coarsens that of G, hence #orbits(H) <= #orbits(G). Verified
    by exact union-find over the real group action on points and on ordered
    pairs, across explicit subgroup families of S_4 and S_5. Anchor facts:
    S_n => exactly 1 orbit (everything interchangeable; zero distinctions);
    the trivial group => n orbits (everything distinct; maximal distinctions)."""
    name = "check_L_orbit_count_monotone_in_symmetry"
    fails = []

    for n in (4, 5):
        fam = build_family(n)
        by = {g["name"]: g for g in fam}

        Sn = by["S%d" % n]
        En = by["E%d" % n]
        if Sn["num_orbits"] != 1:
            fails.append("n=%d: S_n must have exactly 1 orbit, got %d"
                         % (n, Sn["num_orbits"]))
        if En["num_orbits"] != n:
            fails.append("n=%d: trivial group must have %d orbits, got %d"
                         % (n, n, En["num_orbits"]))

        pairs = inclusion_pairs(fam)
        if not pairs:
            fails.append("n=%d: no inclusion pairs found (family too thin)" % n)
        for G, H in pairs:
            # G < H  =>  H no more orbits than G, on points AND ordered pairs
            if not (H["num_orbits"] <= G["num_orbits"]):
                fails.append("n=%d: %s < %s but #orbits(X) %d > %d"
                             % (n, G["name"], H["name"],
                                H["num_orbits"], G["num_orbits"]))
            if not (H["num_pair_orbits"] <= G["num_pair_orbits"]):
                fails.append("n=%d: %s < %s but #orbits(XxX) %d > %d"
                             % (n, G["name"], H["name"],
                                H["num_pair_orbits"], G["num_pair_orbits"]))

    passed = (len(fails) == 0)
    return {
        "name": name,
        "passed": passed,
        "epistemic": "[P_math]",
        "physical_premises_certified": False,
        "tier": 4,
        "key_result": (
            "For G <= H <= S_n acting on a finite carrier X, #orbits(H) <= "
            "#orbits(G): larger symmetry groups induce coarser distinguishability "
            "partitions. S_n => 1 orbit (nothing distinguished); trivial group "
            "=> n orbits (everything distinguished). Verified on {S_4, S_5} by "
            "exact union-find orbit enumeration over explicit subgroup families, "
            "on points and ordered pairs; every real inclusion pair checked."
        ),
        "cross_refs": list(_CROSS_REFS),
        "may_not_cite": list(_MAY_NOT_CITE_COMMON),
        "fail_reasons": fails,
    }


# ============================================================================
# CHECK 2 -- the cost floor sits at maximal symmetry   [P_structural]
# ============================================================================

def check_L_cost_floor_at_maximal_symmetry():
    """[P_structural] With cost(config) = eps* x (#pairs the configuration
    separates) and eps* = 1 > 0 (MD's positive floor), the maximally symmetric
    configuration S_n (one orbit) separates no pair, so its cost is 0 and it
    sits at the cost floor; cost is monotone along the subgroup lattice; and any
    symmetry-break that separates a previously-merged pair strictly raises cost.

    Given the cost model and non-negativity, "max symmetry = floor" is
    elementary: S_n separates nothing, so 0 is the minimum of a set of
    non-negative costs. The content of the check is that MD's positive floor is
    what supplies that non-negativity. Fail-control (existential, not
    universal): there EXISTS an MD-violating cost assignment under which S_n is
    NOT the minimum -- the sign-flip eps* < 0 (which sends the argmin to the
    trivial group E_n, the most-separated configuration) and the {0,1}|{2,..}
    cancelling scheme (which drops a broken configuration strictly below S_n).
    The check requires both witnesses to bite; if neither did, MD's positivity
    would be idle here. This does NOT assert that any weakening of MD breaks the
    floor -- only that at least one MD-violating assignment does."""
    name = "check_L_cost_floor_at_maximal_symmetry"
    fails = []
    eps = Fraction(1)  # eps* > 0 : MD's positive floor

    for n in (4, 5):
        fam = build_family(n)
        Sn_name = "S%d" % n
        En_name = "E%d" % n

        # ---- positive-floor regime (MD) -----------------------------------
        cost_pos = {g["name"]: config_cost(g, eps, "positive") for g in fam}
        min_pos = min(cost_pos.values())
        argmin_pos = [k for k, v in cost_pos.items() if v == min_pos]

        if min_pos != 0:
            fails.append("n=%d: positive-floor min cost is %s, expected 0"
                         % (n, min_pos))
        if cost_pos[Sn_name] != 0:
            fails.append("n=%d: max-symmetry cost is %s, expected 0"
                         % (n, cost_pos[Sn_name]))
        if Sn_name not in argmin_pos:
            fails.append("n=%d: S_n is not a floor-achiever under positive floor"
                         % n)
        if any(v < 0 for v in cost_pos.values()):
            fails.append("n=%d: negative cost under positive floor "
                         "(MD violated internally)" % n)

        # ---- symmetry-breaking strictly raises cost on refining breaks ----
        for G, H in inclusion_pairs(fam):
            cG, cH = cost_pos[G["name"]], cost_pos[H["name"]]
            if not (cH <= cG):
                fails.append("n=%d: cost not monotone on %s < %s (%s !<= %s)"
                             % (n, G["name"], H["name"], cH, cG))
            if G["num_orbits"] > H["num_orbits"] and not (cG > cH):
                fails.append("n=%d: partition-refining break %s -> %s did not "
                             "strictly raise cost (%s vs %s)"
                             % (n, H["name"], G["name"], cG, cH))
            if G["num_orbits"] == H["num_orbits"] and cG != cH:
                fails.append("n=%d: equal orbit partition but unequal cost "
                             "(%s=%s vs %s=%s)"
                             % (n, G["name"], cG, H["name"], cH))

        # ---- MD witness 1: the clean sign-flip control (eps* < 0) ---------
        # Drop MD's POSITIVITY by flipping the floor's sign. With every
        # distinction now weighing eps* < 0, cost = eps* x (#separated pairs) is
        # most negative where the most pairs are separated -- so the argmin moves
        # off S_n onto the trivial group E_n (the most-separated configuration),
        # automatically and with no hand-chosen weights. A non-arbitrary witness
        # that MD's positive floor is what pins the minimum at S_n. The check
        # FAILS if this flip does not occur.
        cost_neg = {g["name"]: config_cost(g, Fraction(-1), "positive")
                    for g in fam}
        min_neg = min(cost_neg.values())
        argmin_neg = [k for k, v in cost_neg.items() if v == min_neg]
        if Sn_name in argmin_neg:
            fails.append("n=%d: sign-flip (eps*<0) still leaves S_n at the "
                         "minimum -- MD's positivity is not biting" % n)
        if argmin_neg != [En_name]:
            fails.append("n=%d: sign-flip (eps*<0) argmin is %s; expected the "
                         "trivial group [%s] (most-separated config) to take "
                         "the minimum" % (n, argmin_neg, En_name))

        # ---- MD witness 2: the cancelling scheme (mixed-sign weights) -----
        # A second MD-violating assignment: distinctions straddling {0,1}|{2,..}
        # weigh -1. Some broken configuration then drops strictly below S_n.
        cost_can = {g["name"]: config_cost(g, eps, "cancelling") for g in fam}
        min_can = min(cost_can.values())
        argmin_can = [k for k, v in cost_can.items() if v == min_can]
        if Sn_name in argmin_can:
            fails.append("n=%d: cancelling scheme still leaves S_n at the "
                         "minimum -- this MD-violating witness did not bite" % n)
        if not (min_can < 0):
            fails.append("n=%d: cancelling scheme produced no sub-floor cost "
                         "-- this MD-violating witness did not bite" % n)

    passed = (len(fails) == 0)
    mnc = list(_MAY_NOT_CITE_COMMON) + [
        "Converse is FALSE. Minimal (floor) cost does NOT imply maximal "
        "symmetry: the floor (cost 0) is achieved by EVERY transitive "
        "configuration (single orbit). S_n is the maximal floor-achiever, not "
        "the unique one. The lemma is the one-way 'max symmetry => floor.'",
        "'Breaking a symmetry always costs' is FALSE. Only breaks that SEPARATE "
        "a previously-merged pair (refine the orbit partition) cost; internal "
        "breaks that preserve the partition (S_n -> A_n, S_n -> C_n) are free "
        "on the point-distinction ledger. Cost is a function of the orbit "
        "PARTITION, not of the group.",
    ]
    return {
        "name": name,
        "passed": passed,
        "epistemic": "[P_structural]",
        "physical_premises_certified": False,
        "tier": 4,
        "key_result": (
            "Under MD's positive floor (eps* > 0, no cancellation), "
            "cost(config) = eps* x (#separated pairs) is minimized (= 0) by the "
            "maximally symmetric configuration S_n, which separates no pair; "
            "cost is monotone along the subgroup lattice and any partition-"
            "refining break strictly raises it. Given non-negativity this is "
            "elementary; MD's role is to supply that non-negativity. Witnessed "
            "existentially: there EXIST MD-violating cost assignments under "
            "which S_n is not the minimum -- the sign-flip eps* < 0 sends the "
            "argmin to the trivial group E_n, and a {0,1}|{2,..} cancelling "
            "scheme drops a broken configuration strictly below S_n. Verified "
            "exactly over subgroup families of S_4 and S_5."
        ),
        "cross_refs": list(_CROSS_REFS),
        "may_not_cite": mnc,
        "fail_reasons": fails,
    }


# ============================================================================
# Bank contract surface
# ============================================================================

_CHECKS = {
    "check_L_orbit_count_monotone_in_symmetry":
        check_L_orbit_count_monotone_in_symmetry,
    "check_L_cost_floor_at_maximal_symmetry":
        check_L_cost_floor_at_maximal_symmetry,
}


def register(registry):
    """Register both checks into a bank-style registry dict (research lane --
    NOT auto-wired; this module is not yet listed in the manifest)."""
    for nm, fn in _CHECKS.items():
        registry[nm] = fn
    return registry


# ============================================================================
# Fail-control recomputation helpers (genuine recomputation, not restated flag)
# ============================================================================

def _recompute_orbit_monotone(n, direction):
    """Recompute the point-orbit monotonicity predicate over every real
    inclusion pair. direction='correct' tests the true claim
    (#orbits(H) <= #orbits(G)); direction='reversed' tests the WRONG claim
    (#orbits(H) >= #orbits(G)). Returns (holds, witness)."""
    fam = build_family(n)
    for G, H in inclusion_pairs(fam):
        og, oh = G["num_orbits"], H["num_orbits"]
        cond = (oh <= og) if direction == "correct" else (oh >= og)
        if not cond:
            return False, (G["name"], H["name"], og, oh)
    return True, None


def _recompute_sn_num_orbits(n, broken):
    """S_n's orbit count via the REAL union-find (broken=False) vs. a stub that
    ignores the group and returns n singletons (broken=True). Shows the
    S_n => 1 orbit anchor tracks the real computation, not a stored constant."""
    Sn = generate_group(_sn_gens(n), n)
    if broken:
        orb = [[i] for i in range(n)]      # hardcode-style cheat: ignore action
    else:
        orb = orbits_on_points(Sn, n)      # real enumeration
    return len(orb)


# ============================================================================
# run_all -- verify, demonstrate fail-controls, print the report
# ============================================================================

def run_all():
    line = "=" * 74
    print(line)
    print("APF bank module : symmetry_cost_floor.py")
    print("registered in BANK_REGISTRY_MODULES since v24.3.437")
    print(line)

    results = {nm: fn() for nm, fn in _CHECKS.items()}

    # ---- [A] check verdicts -------------------------------------------------
    print("\n[A] CHECK VERDICTS")
    for nm, r in results.items():
        print("  %-44s %-14s passed=%s" % (nm, r["epistemic"], r["passed"]))
        for fr in r["fail_reasons"]:
            print("        FAIL: %s" % fr)

    # ---- [B] exact orbit enumeration ---------------------------------------
    print("\n[B] EXACT ORBIT ENUMERATION (union-find over the real group action)")
    for n in (4, 5):
        fam = build_family(n)
        cpairs = n * (n - 1) // 2
        print("\n  X = {0..%d}   (C(n,2) = %d unordered pairs)" % (n - 1, cpairs))
        print("  %-14s %5s %11s %13s %10s"
              % ("subgroup", "order", "#orbits(X)", "#orbits(XxX)", "sep.pairs"))
        for g in fam:
            print("  %-14s %5d %11d %13d %10d"
                  % (g["name"], g["order"], g["num_orbits"],
                     g["num_pair_orbits"], g["num_sep"]))
        incl = inclusion_pairs(fam)
        strict = [(G, H) for G, H in incl if H["num_orbits"] < G["num_orbits"]]
        print("  inclusion pairs checked: %d  (all satisfy #orbits(H) <= "
              "#orbits(G))" % len(incl))
        print("  strict (symmetry actually merges points): %d" % len(strict))
        for G, H in strict:
            print("    %-12s < %-12s : %d -> %d orbits"
                  % (G["name"], H["name"], G["num_orbits"], H["num_orbits"]))

    # ---- [C] check-1 fail-controls (real recomputation) --------------------
    print("\n[C] CHECK-1 FAIL-CONTROLS (genuine recomputation, not a restated "
          "flag)")
    fc1_ok = True
    for n in (4, 5):
        ok_c, _ = _recompute_orbit_monotone(n, "correct")
        ok_r, wit = _recompute_orbit_monotone(n, "reversed")
        real = _recompute_sn_num_orbits(n, broken=False)
        brk = _recompute_sn_num_orbits(n, broken=True)
        print("  n=%d: correct-direction predicate        -> %s   (expect True)"
              % (n, ok_c))
        print("  n=%d: WRONG-direction predicate (>=)      -> %s   (expect False)"
              "   witness=%s" % (n, ok_r, wit))
        print("  n=%d: S_n #orbits  real=%d (==1? %s)   stubbed-cheat=%d "
              "(==1? %s)" % (n, real, real == 1, brk, brk == 1))
        if not (ok_c is True and ok_r is False and real == 1 and brk != 1):
            fc1_ok = False
    print("  -> check-1 mutations demonstrably flip the verdict: %s" % fc1_ok)

    # ---- [D] cost-floor tables (positive floor vs cancelling) --------------
    print("\n[D] COST-FLOOR TABLE   cost = eps* x (#separated pairs), "
          "eps* = 1 (MD positive floor)")
    for n in (4, 5):
        fam = build_family(n)
        print("\n  n=%d:" % n)
        print("  %-14s %8s %6s %14s %14s"
              % ("config", "#orbits", "#sep", "cost(+floor)", "cost(cancel)"))
        for g in fam:
            cp = config_cost(g, Fraction(1), "positive")
            cc = config_cost(g, Fraction(1), "cancelling")
            print("  %-14s %8d %6d %14s %14s"
                  % (g["name"], g["num_orbits"], g["num_sep"], str(cp), str(cc)))
        cost_pos = {g["name"]: config_cost(g, Fraction(1), "positive")
                    for g in fam}
        min_pos = min(cost_pos.values())
        amp = [k for k, v in cost_pos.items() if v == min_pos]
        print("  positive floor : min cost = %s  argmin = %s   (S%d at floor: %s)"
              % (min_pos, amp, n, ("S%d" % n) in amp))

    # ---- [E] MD fail-controls: existential witnesses that positivity is not idle
    print("\n[E] MD FAIL-CONTROLS "
          "(existential: MD-violating assignments that move the minimum off S_n)")
    fc2_ok = True
    for n in (4, 5):
        fam = build_family(n)
        Sn = "S%d" % n

        def amin(mode, eps):
            d = {g["name"]: config_cost(g, eps, mode) for g in fam}
            m = min(d.values())
            return m, [k for k, v in d.items() if v == m]

        mp, ap = amin("positive", Fraction(1))     # MD floor
        ms, as_ = amin("positive", Fraction(-1))   # eps* < 0 (sign flip)
        mc, ac = amin("cancelling", Fraction(1))   # mixed-sign cancellation

        print("  n=%d  +floor (eps*>0)   min=%-3s argmin=%-28s S%d at floor: %s"
              % (n, str(mp), str(ap), n, Sn in ap))
        print("       sign-flip eps*<0   min=%-3s argmin=%-28s S%d at floor: %s"
              "  <- witness 1" % (str(ms), str(as_), n, Sn in as_))
        print("       cancelling weights min=%-3s argmin=%-28s S%d at floor: %s"
              "  <- witness 2" % (str(mc), str(ac), n, Sn in ac))
        # each MD-violating witness must actually move the minimum off S_n
        if Sn in as_ or Sn in ac or not (ms < 0 and mc < 0):
            fc2_ok = False
    print("  -> MD-violating witnesses move the minimum off S_n (existential): %s"
          % fc2_ok)

    # ---- [F] summary --------------------------------------------------------
    overall = all(r["passed"] for r in results.values())
    all_ok = overall and fc1_ok and fc2_ok
    print("\n[F] SUMMARY")
    print("  check_L_orbit_count_monotone_in_symmetry : %s  [P_math]"
          % results["check_L_orbit_count_monotone_in_symmetry"]["passed"])
    print("  check_L_cost_floor_at_maximal_symmetry   : %s  [P_structural]"
          % results["check_L_cost_floor_at_maximal_symmetry"]["passed"])
    print("  check-1 fail-controls flip               : %s" % fc1_ok)
    print("  check-2 MD witnesses bite                : %s" % fc2_ok)
    print("  OVERALL                                  : %s"
          % ("PASS" if all_ok else "FAIL"))
    print(line)
    return {
        "results": results,
        "overall": overall,
        "fail_controls_flip": fc1_ok and fc2_ok,
        "all_ok": all_ok,
    }


if __name__ == "__main__":
    run_all()
