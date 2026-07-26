"""
refining_break_candidate.py
===========================

RESEARCH-LANE BANK **CANDIDATE** -- NOT WIRED INTO THE LIVE BANK.
Self-contained. stdlib only (fractions, itertools). No numpy / scipy / apf / pool.

WHAT THIS SETTLES
-----------------
Background lemma (already audited, taken as GIVEN here):

    cost = enforced distinctions; cost tracks the ORBIT PARTITION of a
    configuration's symmetry group, not the group itself. Only a
    PARTITION-REFINING break (one that separates a previously-merged pair)
    costs. A break to a still-TRANSITIVE subgroup (e.g. S_n -> A_n) is FREE
    (the one-block partition is unchanged).

Question: is the physical "hidden order" -- a preferred foliation of
spacetime, or a directed communication bit -- a partition-REFINING break
(hence charged) or a free transitive break?

Answer proved + tested here: it is a POINT-STABILIZER break, and every
point-stabilizer of a transitive action strictly refines. Hence charged in
the finite enforced-distinction ledger.

THE THEOREM (elementary, but real)
----------------------------------
Let a finite group G act TRANSITIVELY on a carrier C, |C| >= 2, and fix
x in C. Let G_x = { g in G : g.x = x } be the point-stabilizer. Then:

  (i)   G has exactly one orbit (transitivity)              -> 1 block.
  (ii)  {x} is a complete G_x-orbit (every g in G_x fixes x).
  (iii) |C| >= 2 gives some y != x; y lies in a G_x-orbit that cannot
        contain x (orbits partition C, and {x} is already a whole orbit),
        so y is SEPARATED from x.
  ==>   G_x has >= 2 orbits; its orbit partition STRICTLY REFINES the
        one-block G partition. On the enforced-distinction ledger
        (cost = # pairs in different blocks): cost(G) = 0, cost(G_x) > 0.

Nothing in (i)-(iii) uses anything beyond "orbits partition the carrier"
and "|C| >= 2". It is airtight for finite groups.

THE FAIL-CONTROL (why this is about SEPARATION, not group size)
---------------------------------------------------------------
A break to a still-TRANSITIVE proper subgroup H < G keeps the one-block
partition, so cost(H) = 0 even though |H| < |G|. Exhibited on S_n -> A_n
and D_n -> C_n: a SMALLER group with the SAME (zero) cost. Contrast: an
INTRANSITIVE proper subgroup (C_4 -> C_2) DOES cost. So the discriminator
is point-separation (transitivity), not properness / size.

HONEST VERDICT (is anything smuggled? does the reading hold up?)
---------------------------------------------------------------
* "Point-stabilizer of a transitive action always strictly refines" IS a
  real theorem here -- proof above, verified by real enumeration below.
  The ONE definitional input is "cost = # separated pairs" (the ledger),
  which is the background lemma's definition, not something re-derived in
  this module. Given that ledger, cost(G_x) > 0 is FORCED. No hidden True,
  no always-true comparison: the mutation controls flip the checks to
  False when the stabilizer filter or the orbit union-find is corrupted.

* Toner-Bacon directed bit == break of exchange S_2 on {sender, receiver}:
  TIGHT. S_2 is genuinely finite and transitive; a directed bit genuinely
  drops the symmetry to the identity (fixing who sends), cost exactly 1.
  Not forcing anything.

* Preferred foliation == point-stabilizer of the preferred timelike
  direction: STRUCTURALLY SOUND but a READING. Lorentz really does act
  transitively on future timelike directions, and the preferred-frame
  little group really is that direction's stabilizer (SO(3)). BUT the real
  group is an infinite Lie group, not the finite proxy used here; the
  finite "# separated pairs" count does NOT transfer as a number to the
  infinite direction space. Only the QUALITATIVE jump (cost 0 -> cost > 0)
  is read across. Pushed to a quantitative charge, or claimed as
  A1-derived, it WOULD be forcing the analogy. Fenced accordingly.

WHAT THIS DOES NOT DO (fences, carried on every check's may_not_cite)
--------------------------------------------------------------------
* Does NOT show APF *charges* the order -- that needs enforcement-realism.
* Does NOT lift the QAC -- still needs enforcement-realism + origin-forcing
  (G-hold-exact is now constitutively free under A2-exact, Ethan's ruling
  2026-07-26).
* "foliation = point-stabilizer of the frame action" is a modeling READING.
"""

from fractions import Fraction
import itertools


# ---------------------------------------------------------------------------
# Permutation / group machinery -- exact, stdlib only.
# A permutation on n points is a tuple p of length n with p[i] = image of i.
# The action is g.x = g[x].  Composition (p after q): (p o q)[i] = p[q[i]].
# ---------------------------------------------------------------------------

def identity(n):
    return tuple(range(n))


def compose(p, q):
    """p after q:  apply q, then p."""
    return tuple(p[q[i]] for i in range(len(q)))


def inverse(p):
    n = len(p)
    inv = [0] * n
    for i in range(n):
        inv[p[i]] = i
    return tuple(inv)


def permutation_sign(p):
    """+1 for even, -1 for odd, via cycle-parity."""
    n = len(p)
    seen = [False] * n
    sign = 1
    for i in range(n):
        if not seen[i]:
            j = i
            length = 0
            while not seen[j]:
                seen[j] = True
                j = p[j]
                length += 1
            if length % 2 == 0:      # an even-length cycle is an odd permutation
                sign = -sign
    return sign


def is_group(G, n):
    """Real closure/identity/inverse check -- confirms the constructors
    actually produce groups (teeth against a broken generator set)."""
    Gset = set(G)
    if len(Gset) != len(G):
        return False, "duplicate elements"
    if identity(n) not in Gset:
        return False, "no identity"
    for g in G:
        if inverse(g) not in Gset:
            return False, "missing inverse"
    for a in G:
        for b in G:
            if compose(a, b) not in Gset:
                return False, "not closed"
    return True, "ok"


def symmetric_group(n):
    return [tuple(p) for p in itertools.permutations(range(n))]


def alternating_group(n):
    return [g for g in symmetric_group(n) if permutation_sign(g) == 1]


def cyclic_group(n):
    """Regular cyclic action C_n on n points, generated by 0->1->...->n-1->0.
    Returned as [e, c, c^2, ..., c^(n-1)]."""
    c = tuple((i + 1) % n for i in range(n))
    G = []
    g = identity(n)
    for _ in range(n):
        G.append(g)
        g = compose(c, g)
    return G


def dihedral_group(n):
    """D_n on the n vertices of a regular n-gon: n rotations + n reflections.
    Reflection through vertex 0:  i -> (-i) mod n."""
    rot = cyclic_group(n)
    refl0 = tuple((-i) % n for i in range(n))
    G = list(rot) + [compose(r, refl0) for r in rot]
    return list(dict.fromkeys(G))   # dedupe, preserve order


# ---------------------------------------------------------------------------
# Orbits (union-find over the real action), stabilizers, and the ledger.
# ---------------------------------------------------------------------------

def orbit_partition(H, n):
    """Orbit partition of C = {0..n-1} under H, by real union-find over the
    action.  Returns a list of frozensets."""
    parent = list(range(n))

    def find(a):
        r = a
        while parent[r] != r:
            r = parent[r]
        while parent[a] != r:      # path compression
            parent[a], a = r, parent[a]
        return r

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for h in H:
        for p in range(n):
            union(p, h[p])

    blocks = {}
    for p in range(n):
        blocks.setdefault(find(p), []).append(p)
    return [frozenset(v) for v in blocks.values()]


def stabilizer(G, x):
    """Point-stabilizer G_x = { g in G : g.x = x }, by actual filtering."""
    return [g for g in G if g[x] == x]


def is_transitive(G, n):
    return n >= 1 and len(orbit_partition(G, n)) == 1


def separated_pairs(partition, n):
    """Explicit enumeration of the pairs (i<j) that lie in DIFFERENT blocks.
    This is the enforced-distinction ledger's raw content."""
    block_of = {}
    for bi, blk in enumerate(partition):
        for p in blk:
            block_of[p] = bi
    sep = []
    for i in range(n):
        for j in range(i + 1, n):
            if block_of[i] != block_of[j]:
                sep.append((i, j))
    return sep


def cost(H, n):
    """cost(H) = number of pairs separated by the H-orbit partition."""
    return len(separated_pairs(orbit_partition(H, n), n))


def refines(fine, coarse):
    """Every block of `fine` sits inside some block of `coarse`."""
    return all(any(fb <= cb for cb in coarse) for fb in fine)


def strictly_refines(fine, coarse):
    return refines(fine, coarse) and len(fine) > len(coarse)


def relabel(G, sigma):
    """Conjugate the action by a relabeling sigma of the carrier:
    the relabeled g' satisfies  g'[sigma[i]] = sigma[g[i]]  (i.e. sigma g sigma^-1)."""
    n = len(sigma)
    out = []
    for g in G:
        ng = [0] * n
        for i in range(n):
            ng[sigma[i]] = sigma[g[i]]
        out.append(tuple(ng))
    return out


# ---------------------------------------------------------------------------
# Corruptible core (dependency injection lets the mutation controls flip it).
# ---------------------------------------------------------------------------

def _verify_transitive_refinement(G, n, x, stab_fn, orb_fn):
    """Returns (passed, details, reasons). `stab_fn`/`orb_fn` are injected so
    a corrupted stabilizer or a corrupted orbit union-find must flip passed."""
    reasons = []
    details = {}

    okg, msg = is_group(G, n)
    if not okg:
        reasons.append("G is not a group: %s" % msg)

    Gpart = orb_fn(G, n)
    details["G_orbits"] = len(Gpart)
    if len(Gpart) != 1:
        reasons.append("G not transitive: %d orbits" % len(Gpart))

    Gx = stab_fn(G, x)
    okgx, msg = is_group(Gx, n)
    if not okgx:
        reasons.append("G_x is not a group: %s" % msg)

    Gxpart = orb_fn(Gx, n)
    details["Gx_orbits"] = len(Gxpart)

    x_block = next(b for b in Gxpart if x in b)
    if x_block != frozenset({x}):
        reasons.append("{x} is not a singleton G_x-orbit: got %s" % sorted(x_block))

    if len(Gxpart) < 2:
        reasons.append("G_x did not refine: %d orbit(s)" % len(Gxpart))

    if not strictly_refines(Gxpart, Gpart):
        reasons.append("G_x-partition does not strictly refine the G-partition")

    sep_G = separated_pairs(Gpart, n)
    sep_Gx = separated_pairs(Gxpart, n)
    details["cost_G"] = len(sep_G)
    details["cost_Gx"] = len(sep_Gx)
    if len(sep_G) != 0:
        reasons.append("cost(G) != 0: %d" % len(sep_G))
    if len(sep_Gx) <= 0:
        reasons.append("cost(G_x) not positive: %d" % len(sep_Gx))

    sepset = set(sep_Gx)
    x_separated = all((min(x, y), max(x, y)) in sepset for y in range(n) if y != x)
    if not x_separated:
        reasons.append("x is not separated from every other point")

    return (len(reasons) == 0), details, reasons


# ---------------------------------------------------------------------------
# Test inventory.
# ---------------------------------------------------------------------------

_TEST_CASES = [
    # (label, G, n, x)
    ("S_3 on {0,1,2}",   symmetric_group(3), 3, 0),
    ("S_4 on {0..3}",    symmetric_group(4), 4, 0),
    ("S_5 on {0..4}",    symmetric_group(5), 5, 0),
    ("C_4 on {0..3}",    cyclic_group(4),    4, 0),
    ("C_5 on {0..4}",    cyclic_group(5),    5, 0),
    ("D_4 on {0..3}",    dihedral_group(4),  4, 0),
    ("D_3 on {0,1,2}",   dihedral_group(3),  3, 0),
    ("S_2 on {A,B}",     symmetric_group(2), 2, 0),
]

_BREAK_CASES = [
    # (label, G, H, n)  where H is a TRANSITIVE proper subgroup of G
    ("S_3 -> A_3",             symmetric_group(3), alternating_group(3), 3),
    ("S_4 -> A_4",             symmetric_group(4), alternating_group(4), 4),
    ("S_5 -> A_5",             symmetric_group(5), alternating_group(5), 5),
    ("D_4 -> C_4 (rotations)", dihedral_group(4),  cyclic_group(4),      4),
    ("D_3 -> C_3 (rotations)", dihedral_group(3),  cyclic_group(3),      3),
]


_CROSS_REFS = [
    "prior lemma: cost tracks the orbit PARTITION, not the group (already audited)",
    "enforced-distinction ledger (cost = # separated pairs)",
    "orbit-stabilizer / transitive-action structure",
    "QAC (quantum admissibility condition) -- fenced, not touched",
    "symmetry_cost_floor",
    "rent_exclusion_gate",
    "occupant_cost_selection",
    "check_T_third_boat_iff_local",
    "T_ledger_rent_excluded",
]

_FENCES_COMMON = [
    "Shows the order is a partition-REFINING break IN THE FINITE MODEL only.",
    "Does NOT establish that APF CHARGES the order -- enforcement-realism is a separate step.",
    "Does NOT lift the QAC (still needs enforcement-realism + origin-forcing; G-hold-exact is now constitutively free under A2-exact, Ethan's ruling 2026-07-26).",
]

_FENCES_READING = _FENCES_COMMON + [
    "'foliation = point-stabilizer of the frame action' is a modeling READING, not an A1-derivation.",
    "The Lorentz group is infinite; the finite group is a structural proxy. Only the qualitative "
    "0 -> positive jump is read across -- the numeric charge is a finite-model artifact.",
    "Even the qualitative 0 -> positive transfer to the continuum Lorentz case is an analogy, "
    "not a proven jump -- the enforced-distinction ledger is undefined on the continuum of directions.",
]


# ---------------------------------------------------------------------------
# Checks (bank contract).
# ---------------------------------------------------------------------------

def check_L_point_stabilizer_refines():
    """[P_math] The general theorem, verified by real enumeration."""
    name = "check_L_point_stabilizer_refines"
    rows = []
    fail_reasons = []
    for label, G, n, x in _TEST_CASES:
        ok, det, reasons = _verify_transitive_refinement(G, n, x, stabilizer, orbit_partition)
        Gx = stabilizer(G, x)
        rows.append({
            "case": label, "|G|": len(G), "|G_x|": len(Gx),
            "G_orbits": det.get("G_orbits"), "Gx_orbits": det.get("Gx_orbits"),
            "cost_G": det.get("cost_G"), "cost_Gx": det.get("cost_Gx"),
        })
        if not ok:
            fail_reasons.extend("%s: %s" % (label, r) for r in reasons)
    passed = (len(fail_reasons) == 0)
    return {
        "name": name, "tier": 4, "epistemic": "P_math",
        "physical_premises_certified": False,
        "passed": passed,
        "key_result": {
            "statement": (
                "For every transitive finite G on C (|C|>=2) and x in C, the "
                "point-stabilizer G_x has {x} as a singleton orbit and strictly "
                "refines the one-block G-partition: cost(G)=0, cost(G_x)>0."),
            "verified_cases": rows,
        },
        "cross_refs": list(_CROSS_REFS),
        "may_not_cite": list(_FENCES_COMMON),
        "fail_reasons": fail_reasons,
    }


def _presentation_invariance_probe():
    """Cost, and the stabilizer's conjugation, are invariant under relabeling
    the carrier -- so the 'charge' is presentation-invariant (real teeth)."""
    reasons = []
    G = symmetric_group(4)
    n, x = 4, 0
    sigma = (1, 2, 3, 0)            # a nontrivial relabeling of the four points
    Gr = relabel(G, sigma)
    if cost(G, n) != cost(Gr, n):
        reasons.append("cost of G not invariant under relabeling")
    Gx = stabilizer(G, x)
    Gxr = relabel(Gx, sigma)
    if cost(Gx, n) != cost(Gxr, n):
        reasons.append("cost of G_x not invariant under relabeling")
    # stabilizers conjugate:  stab(sigma G sigma^-1, sigma[x]) == sigma (stab(G,x)) sigma^-1
    if set(stabilizer(Gr, sigma[x])) != set(Gxr):
        reasons.append("stabilizer does not conjugate correctly under relabeling")
    return {
        "ok": len(reasons) == 0,
        "reasons": reasons,
        "note": "cost(S_4)=%d == cost(relabelled)=%d; G_0 conjugates to the stabilizer of point %d; "
                "cost(G_0)=%d == cost(relabelled G_0)=%d"
                % (cost(G, n), cost(Gr, n), sigma[x], cost(Gx, n), cost(Gxr, n)),
    }


def check_T_order_charge_positive():
    """[P_math] The comparison: cost(ordered) - cost(symmetric) is strictly
    positive and presentation-invariant -- the charge for the order."""
    name = "check_T_order_charge_positive"
    fail_reasons = []
    rows = []
    for label, G, n, x in _TEST_CASES:
        cG = cost(G, n)
        Gx = stabilizer(G, x)
        cGx = cost(Gx, n)
        charge = Fraction(cGx - cG)         # exact; counts are integers
        rows.append({"case": label, "cost_symmetric": cG,
                     "cost_ordered": cGx, "charge": str(charge)})
        if cG != 0:
            fail_reasons.append("%s: symmetric config cost != 0 (%d)" % (label, cG))
        if not (charge > 0):
            fail_reasons.append("%s: charge not strictly positive (%s)" % (label, charge))
    inv = _presentation_invariance_probe()
    if not inv["ok"]:
        fail_reasons.extend(inv["reasons"])
    passed = (len(fail_reasons) == 0)
    return {
        "name": name, "tier": 4, "epistemic": "P_math",
        "physical_premises_certified": False,
        "passed": passed,
        "key_result": {
            "statement": (
                "For every transitive finite G on C (|C|>=2) and x in C, the "
                "point-stabilizer configuration carries a strictly positive, "
                "presentation-invariant cost relative to the transitive "
                "configuration: charge = cost(G_x) - cost(G) > 0, exact (integer "
                "counts) and invariant under relabeling the carrier. The physical "
                "account-identification (orthodox<->transitive, "
                "hidden-order<->point-stabilizer) is deferred to "
                "check_T_physical_reading [P_structural_reading]."),
            "charges": rows,
            "presentation_invariance": inv["note"],
        },
        "cross_refs": list(_CROSS_REFS),
        "may_not_cite": list(_FENCES_COMMON),
        "fail_reasons": fail_reasons,
    }


def check_T_transitive_break_is_free():
    """[P_math] FAIL-CONTROL. A break to a still-TRANSITIVE proper subgroup
    costs 0 even though the group shrank -- which exhibits/confirms that the
    ledger (taken as GIVEN) reads point-SEPARATION, not group size. Contrasted
    with an intransitive break (C_4 -> C_2) which DOES cost."""
    name = "check_T_transitive_break_is_free"
    fail_reasons = []
    rows = []
    for label, G, H, n in _BREAK_CASES:
        okH, msg = is_group(H, n)
        proper = set(H) < set(G)
        smaller = len(H) < len(G)
        trans = is_transitive(H, n)
        cH = cost(H, n)
        rows.append({"break": label, "|G|": len(G), "|H|": len(H),
                     "H_proper_subgroup": proper, "H_transitive": trans, "cost_H": cH})
        if not okH:
            fail_reasons.append("%s: H is not a group (%s)" % (label, msg))
        if not proper:
            fail_reasons.append("%s: H is not a proper subgroup of G" % label)
        if not smaller:
            fail_reasons.append("%s: H is not strictly smaller than G" % label)
        if not trans:
            fail_reasons.append("%s: H is not transitive" % label)
        if cH != 0:
            fail_reasons.append("%s: transitive break cost != 0 (%d)" % (label, cH))

    # Contrast: an INTRANSITIVE proper subgroup DOES cost.
    c4 = cyclic_group(4)               # [e, c, c^2, c^3]
    C2 = [c4[0], c4[2]]                # {e, c^2}, orbits {0,2},{1,3}
    okC2, msgC2 = is_group(C2, 4)
    cost_intrans = cost(C2, 4)
    trans_intrans = is_transitive(C2, 4)
    contrast_row = {"break": "C_4 -> C_2 (intransitive)", "|G|": 4, "|H|": 2,
                    "H_proper_subgroup": set(C2) < set(c4),
                    "H_transitive": trans_intrans, "cost_H": cost_intrans}
    rows.append(contrast_row)
    if not okC2:
        fail_reasons.append("intransitive contrast: C_2 is not a group (%s)" % msgC2)
    if trans_intrans:
        fail_reasons.append("intransitive contrast: C_2 unexpectedly transitive")
    if not (cost_intrans > 0):
        fail_reasons.append("intransitive contrast: expected cost > 0, got %d" % cost_intrans)

    passed = (len(fail_reasons) == 0)
    return {
        "name": name, "tier": 4, "epistemic": "P_math",
        "physical_premises_certified": False,
        "passed": passed,
        "key_result": {
            "statement": (
                "A break to a still-transitive proper subgroup keeps the one-block "
                "partition: cost stays 0 while |group| strictly drops. An intransitive "
                "proper subgroup separates points and DOES cost. The discriminator is "
                "point-separation, not group size."),
            "transitive_breaks": rows[:-1],
            "intransitive_contrast": contrast_row,
        },
        "cross_refs": list(_CROSS_REFS),
        "may_not_cite": list(_FENCES_COMMON),
        "fail_reasons": fail_reasons,
    }


def check_T_physical_reading():
    """[P_structural_reading] The physical identification. Both 'hidden order'
    candidates are point-stabilizer breaks, hence refining by the theorem.
    This is a MODELING READING, heavily fenced -- not an A1-derivation."""
    name = "check_T_physical_reading"
    fail_reasons = []

    # (a) Toner-Bacon directed bit == break of exchange S_2 on {sender, receiver}.
    S2 = symmetric_group(2)
    cost_sym_tb = cost(S2, 2)                 # symmetric channel: parties interchangeable
    directed = stabilizer(S2, 0)              # fix the sender -> {e}
    cost_dir_tb = cost(directed, 2)           # directed bit
    if cost_sym_tb != 0:
        fail_reasons.append("TB: symmetric channel cost != 0 (%d)" % cost_sym_tb)
    if cost_dir_tb != 1:
        fail_reasons.append("TB: directed-bit cost != 1 (%d)" % cost_dir_tb)
    okTB, _, rTB = _verify_transitive_refinement(S2, 2, 0, stabilizer, orbit_partition)
    if not okTB:
        fail_reasons.extend("TB: %s" % r for r in rTB)

    # (b) Preferred foliation == point-stabilizer of the preferred timelike
    #     direction. Finite structural proxy: a transitive group on 'directions'.
    Dir = dihedral_group(6)
    m = 6
    cost_noframe = cost(Dir, m)               # no preferred direction
    little = stabilizer(Dir, 0)               # preferred-direction little group (proxy)
    cost_frame = cost(little, m)              # a preferred foliation
    if cost_noframe != 0:
        fail_reasons.append("foliation proxy: no-frame cost != 0 (%d)" % cost_noframe)
    if not (cost_frame > 0):
        fail_reasons.append("foliation proxy: preferred-frame cost not > 0 (%d)" % cost_frame)
    okFol, _, rFol = _verify_transitive_refinement(Dir, m, 0, stabilizer, orbit_partition)
    if not okFol:
        fail_reasons.extend("foliation: %s" % r for r in rFol)

    passed = (len(fail_reasons) == 0)
    return {
        "name": name, "tier": 4, "epistemic": "P_structural_reading",
        "physical_premises_certified": False,
        "passed": passed,
        "key_result": {
            "statement": (
                "Under the point-stabilizer identification, both 'hidden order' "
                "candidates are refining breaks: a directed communication bit breaks "
                "the party-exchange S_2 to the identity (cost 1); a preferred foliation "
                "is the little group of a preferred direction under the (transitive) "
                "action on directions (cost > 0 in the finite proxy)."),
            "toner_bacon": {
                "model": "S_2 on {sender=0, receiver=1}",
                "cost_symmetric_channel": cost_sym_tb,
                "cost_directed_bit": cost_dir_tb,
                "assessment": "tight -- genuinely finite and transitive; a directed bit "
                              "really drops S_2 to the identity fixing who sends.",
            },
            "foliation": {
                "model": "D_6 on 6 directions as a finite proxy for the transitive "
                         "Lorentz action on timelike directions",
                "cost_no_preferred_frame": cost_noframe,
                "cost_preferred_frame": cost_frame,
                "assessment": "structurally sound but a READING: little group = stabilizer "
                              "is genuinely how preferred frames work, but the real group is "
                              "infinite and the numeric cost is a finite-model artifact; only "
                              "the 0 -> positive jump is read across.",
            },
        },
        "cross_refs": list(_CROSS_REFS) + [
            "Lorentz little group SO(3) as the stabilizer of a timelike direction",
            "Toner-Bacon 2003 directed classical-communication model",
        ],
        "may_not_cite": list(_FENCES_READING),
        "fail_reasons": fail_reasons,
    }


# ---------------------------------------------------------------------------
# Mutation controls (real teeth) + import audit.
# ---------------------------------------------------------------------------

def _mutation_demo():
    """Corrupt the stabilizer, then the orbit union-find; the core verification
    must flip to passed=False in both cases."""
    G = symmetric_group(4)
    n, x = 4, 0
    real_ok, _, _ = _verify_transitive_refinement(G, n, x, stabilizer, orbit_partition)

    corrupt_stab = lambda GG, xx: list(GG)                      # 'stabilizer' = whole group
    corrupt_orb = lambda HH, nn: [frozenset(range(nn))]         # union-find = one block, always

    ok_cs, _, rs_cs = _verify_transitive_refinement(G, n, x, corrupt_stab, orbit_partition)
    ok_co, _, rs_co = _verify_transitive_refinement(G, n, x, stabilizer, corrupt_orb)

    teeth_ok = (real_ok is True) and (ok_cs is False) and (ok_co is False)
    return {
        "real_passes": real_ok,
        "corrupt_stabilizer_passes": ok_cs,
        "corrupt_orbit_unionfind_passes": ok_co,
        "corrupt_stabilizer_fail_reasons": rs_cs,
        "corrupt_orbit_fail_reasons": rs_co,
        "teeth_ok": teeth_ok,
    }


def _source_import_audit():
    """Read this file and confirm only fractions/itertools are imported.
    Returns [] if clean, a list of offending lines otherwise, or None if the
    source is unreadable."""
    allowed = {"fractions", "itertools"}
    bad = []
    try:
        src = open(__file__, "r", encoding="utf-8").read()
    except Exception:
        return None
    for line in src.splitlines():
        s = line.strip()
        if s.startswith("import "):
            mod = s[len("import "):].split()[0].split(".")[0].split(",")[0]
            if mod not in allowed:
                bad.append(s)
        elif s.startswith("from "):
            mod = s[len("from "):].split()[0].split(".")[0]
            if mod not in allowed:
                bad.append(s)
    return bad


# ---------------------------------------------------------------------------
# Bank contract glue.
# ---------------------------------------------------------------------------

_CHECKS = [
    check_L_point_stabilizer_refines,
    check_T_order_charge_positive,
    check_T_transitive_break_is_free,
    check_T_physical_reading,
]


def register(registry):
    """Optional bank hook. This is a RESEARCH-LANE CANDIDATE and is NOT wired
    into the live bank; provided only for contract compatibility."""
    for chk in _CHECKS:
        try:
            registry.register(chk)
        except AttributeError:
            try:
                registry[chk.__name__] = chk
            except Exception:
                pass
    return list(_CHECKS)


def _fmt_table(rows, cols):
    widths = {c: len(c) for c in cols}
    for r in rows:
        for c in cols:
            widths[c] = max(widths[c], len(str(r.get(c, ""))))
    line = "  ".join(c.ljust(widths[c]) for c in cols)
    out = [line, "  ".join("-" * widths[c] for c in cols)]
    for r in rows:
        out.append("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))
    return "\n".join(out)


def run_all():
    results = [chk() for chk in _CHECKS]
    mutation = _mutation_demo()
    import_audit = _source_import_audit()

    all_checks_pass = all(r["passed"] for r in results)
    teeth_ok = mutation["teeth_ok"]
    imports_clean = (import_audit == [] or import_audit is None)
    overall = all_checks_pass and teeth_ok and imports_clean

    lines = []
    lines.append("=" * 78)
    lines.append("refining_break_candidate.py  --  RESEARCH-LANE BANK CANDIDATE (not wired in)")
    lines.append("=" * 78)

    lines.append("\nIMPORT AUDIT (fractions/itertools only): %s"
                 % ("CLEAN" if imports_clean else "DIRTY -> %s" % import_audit))

    lines.append("\n--- CHECK RESULTS ---")
    for r in results:
        lines.append("  [%s] %-38s %s"
                     % ("PASS" if r["passed"] else "FAIL", r["name"], r["epistemic"]))
        if r["fail_reasons"]:
            for fr in r["fail_reasons"]:
                lines.append("        fail_reason: %s" % fr)

    # Theorem enumeration table
    lc = next(r for r in results if r["name"] == "check_L_point_stabilizer_refines")
    lines.append("\n--- THEOREM ENUMERATION (point-stabilizer refines) ---")
    lines.append(_fmt_table(lc["key_result"]["verified_cases"],
                            ["case", "|G|", "|G_x|", "G_orbits", "Gx_orbits", "cost_G", "cost_Gx"]))

    # Charge table
    tc = next(r for r in results if r["name"] == "check_T_order_charge_positive")
    lines.append("\n--- ORDER CHARGE (cost_ordered - cost_symmetric) ---")
    lines.append(_fmt_table(tc["key_result"]["charges"],
                            ["case", "cost_symmetric", "cost_ordered", "charge"]))
    lines.append("  presentation-invariance: " + tc["key_result"]["presentation_invariance"])

    # Fail-control table
    fc = next(r for r in results if r["name"] == "check_T_transitive_break_is_free")
    lines.append("\n--- FAIL-CONTROL: transitive break is FREE (separation, not size) ---")
    allrows = fc["key_result"]["transitive_breaks"] + [fc["key_result"]["intransitive_contrast"]]
    lines.append(_fmt_table(allrows,
                            ["break", "|G|", "|H|", "H_proper_subgroup", "H_transitive", "cost_H"]))

    # Physical reading
    pc = next(r for r in results if r["name"] == "check_T_physical_reading")
    kr = pc["key_result"]
    lines.append("\n--- PHYSICAL READING [P_structural_reading] ---")
    lines.append("  Toner-Bacon: %s | symmetric cost=%d, directed-bit cost=%d"
                 % (kr["toner_bacon"]["model"],
                    kr["toner_bacon"]["cost_symmetric_channel"],
                    kr["toner_bacon"]["cost_directed_bit"]))
    lines.append("    -> %s" % kr["toner_bacon"]["assessment"])
    lines.append("  Foliation:   %s | no-frame cost=%d, preferred-frame cost=%d"
                 % (kr["foliation"]["model"],
                    kr["foliation"]["cost_no_preferred_frame"],
                    kr["foliation"]["cost_preferred_frame"]))
    lines.append("    -> %s" % kr["foliation"]["assessment"])

    # Mutation
    lines.append("\n--- MUTATION CONTROLS (teeth) ---")
    lines.append("  real machinery passes ............... %s" % mutation["real_passes"])
    lines.append("  corrupt stabilizer (=whole group) ... passes=%s (expected False)"
                 % mutation["corrupt_stabilizer_passes"])
    lines.append("  corrupt orbit union-find (1 block) .. passes=%s (expected False)"
                 % mutation["corrupt_orbit_unionfind_passes"])
    lines.append("  teeth_ok = %s" % teeth_ok)
    lines.append("    sample corrupt-stabilizer fail_reasons: %s"
                 % "; ".join(mutation["corrupt_stabilizer_fail_reasons"][:3]))

    lines.append("\n--- OVERALL ---")
    lines.append("  all_checks_pass=%s  teeth_ok=%s  imports_clean=%s  =>  OVERALL %s"
                 % (all_checks_pass, teeth_ok, imports_clean,
                    "PASS" if overall else "FAIL"))
    lines.append("=" * 78)

    print("\n".join(lines))
    return {
        "results": results, "mutation": mutation, "import_audit": import_audit,
        "all_checks_pass": all_checks_pass, "teeth_ok": teeth_ok,
        "imports_clean": imports_clean, "overall": overall,
    }


if __name__ == "__main__":
    summary = run_all()
    raise SystemExit(0 if summary["overall"] else 1)
