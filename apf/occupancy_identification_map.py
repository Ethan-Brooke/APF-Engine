"""The occupancy identification map: type facts and the range obstruction, exactly.

BANKED v24.3.472 (2026-08-12).  Built by a build seat under the Situational
Sign program (identification-map lane) to the FROZEN claim surface (binding;
K1-K5 adopted there verbatim from the scoping return):
  Artifacts_2026-08-11_session/idmap_scoping/CLAIM_SURFACE_FROZEN_2026-08-12.md
  raw sha256: 0744de9bd8cbe925f3438a9325993055f1896cf795e2a27456d2b775700bf8e2
The module may state nothing beyond that surface.  Weakening a claim is the
permitted direction; strengthening is not.

Two blinded cold audits, LAND-WITH-FIXES 0.86 / 0.86, zero arithmetic
disagreement in either; cold fix seat carried (7 fixes, 0 declined); the
build seat caught two frozen-surface errors, both repaired in the weakening
direction (carried in WEAKENINGS below); receipts at
Artifacts_2026-08-11_session/idmap_scoping/.  LIFTED by Ethan's ruling
2026-08-12.  BARE-NAME registry keys per D6@2026-08-03.

WHAT THIS MODULE COMPUTES (exact integer arithmetic on every verdict path;
Z2 carried as +-1 integers; no floats; stdlib only).  Domain vocabulary: an
occupancy input X is read as a membership subset of the sep(P) ground set
{0..n-1} UNDER THE NAMED IMPORT iota (anchor universe <-> per-distinction
realizations; constructed nowhere -- see K5(a)).  Codomain vocabulary: Z2
holonomy characters over fundamental-cycle bases of sep(P), consumed from
the banked continuation_join_network machinery by import (never silently
re-implemented; where a second implementation is needed for an independence
leg, it is compared against the imported one).

K1 (check_K1_coboundary_kill).  Every edge labeling factoring as a
per-vertex function of occupancy data (the XOR/vertex-potential genre) has
the trivial holonomy character on every realizable sep(P) at stated n
(<= 5, exhaustive over all X and all 69 connected sep graphs).  Executed as
a theorem of the coboundary identity exhibited across the class: every
element of the WHOLE cycle space of every graph has all-even vertex
degrees, so the product of chi(i)chi(j) over any element is chi(v)^even = 1
-- verified for ALL 2^n potentials chi (covering every per-vertex
function of occupancy data), on ALL 2^dim cycle-space elements,
on ALL 69 graphs.  The "natural parity" reading of the occupancy candidate
(XOR of membership) is exhibited as a vertex-potential instance and
supplies only the balanced endpoint.

K2 (check_K2_rule_collapse).  Over the eight symmetric Boolean endpoint
rules on occupancy membership (DERIVED by symmetry-filtering all 16 Boolean
functions of two bits, not stipulated; the 8 asymmetric tables are excluded
by that filter -- a stated domain bound, not a theorem computed here: an
asymmetric rule presupposes an edge orientation no import supplies),
exactly one situational class-map
family exists up to the antibalanced involution: {const+, XOR} -> the
balanced endpoint; {const-, XNOR} -> the antibalanced endpoint; {AND, OR}
-> one situational family; {NAND, NOR} -> its antibalanced twist.
Exhaustive over all X and all 69 graphs.  The involution is a NAMED Z2
convention import, fixed by nothing computed in this module.

K3 (check_K3_inhabitation_type_facts).  The membership-AND map is
S_n-equivariant (executed exhaustively at n = 3, 4: label-level transport
identity over every permutation, every X, every >= 2-block partition),
class-valued and cycle-basis-free (two-basis partition identity on all 69
graphs, the bases genuinely differing on 51), attains two classes over one
P wherever dim >= 1 (57 graphs; the N6 R1 shape), a non-endpoint class
wherever dim >= 2 (53 graphs; the R6 presupposition met at the audit's
stated boundary), and is surjective onto all 2^dim switching classes at
every connected sep(P) with n <= 4 and every dim <= 3 graph at n = 5 (43
graphs, verified in genuine switching-class terms by union-find over the
actual switching action, consumed from the join network).  STATED AS TYPE
FACTS about a constructed toy map under two named imports (iota,
endpoint-locality) -- never as a reading of the world.

K4 (check_K4_range_obstruction).  At n = 5 the same map fails surjectivity
on every sep(P) with cyclomatic >= 4: images 14 of 16 (all 15 dim-4
graphs), 20 of 32 (all 10 dim-5 graphs), 22 of 64 (K5) -- exact, and
confirmed on the class side by union-find on all 26 obstructed graphs.
Any supplier factoring through B-valued per-vertex occupancy traces has
image <= B^n, which is smaller than the class count 2^(m-n+1) on K_n from
n = 5 at B = 2, from n = 6 at B = 3, from n = 7 at B = 4, from n = 8 at
B = 5 and B = 6 (exact table, with a per-B permanence induction executed at
its base and step), and from the certified sufficient threshold
n_B = 2*ceil(log2 B) + 4 at every fixed B in 2..64 (executed exactly;
sufficient, not minimal -- B = 2 first-fails at n = 5 while n_B(2) = 6).
THE OBSTRUCTION IS AN
OBSTRUCTION CERTIFICATE ABOUT A CANDIDATE FAMILY -- single-event,
vertex-mediated, fixed per-vertex budget -- NOT about all possible
suppliers; the returned records carry that scope in computed form, and the
named dissolution routes (an edge-indexed tie-event family; a
pairwise-shared-substrate realization supplying per-separated-pair join
data; a derived growing budget schedule) are each an import absent at HEAD.

K5 (check_K5_import_controls).  Permanent controls in the B4/J4 style.
(a) NO map between the QAC anchor universe and any sep(P) ground set is
constructed; the home module's own functions are EXECUTED to exhibit the
two vocabularies as disjoint index sets, and its join-count identity
jA - jB = (b - a)*eps is re-executed through its own _joint/_deficit over
the full 87-case grid (J4(c) carried).  (b) The endpoint-locality
factorization and the antibalanced twist are NAMED IMPORTS at their sites;
the twist control exhibits AND and NAND passing every type requirement
computed here with pointwise-different class-maps on every non-bipartite
graph.  (c) NO identification of the constructed character with the class
the represented side measures -- the S4 NO-CANONICAL-MAP genre bars
assuming it; the module bars the citation, and a set-exact AST probe
enforces that this module imports NO represented-side apf module.  (d)
Magnitude non-supply disclosed and computed at the output level (every
returned character component is a +-1 integer; the scan reads outputs
only); the two
v2-gate structural facts are carried as RECORDS with the gate-design
question routed to Ethan, not answered in-module.

WEAKENINGS CARRIED (permitted direction; each disclosed at its leg):
1. The frozen K2/K5(b) phrase "the involution ... changes the class" /
   "with different images" is weakened to the computed truth: the twist
   changes the CLASS-MAP POINTWISE at every X on exactly the 44
   non-bipartite sep graphs (>= 3 blocks) and is class-neutral on the 25
   bipartite ones; as SETS, the AND and NAND images coincide on all 69
   graphs at stated n (computed).
2. The frozen K4 phrase "from n = 8 at every fixed B" is weakened to
   "from n = 8 at every fixed B <= 6 (computed, permanence induction), and
   from the sufficient threshold n_B = 2*ceil(log2 B) + 4 at every fixed
   B in 2..64 (executed exactly)": the literal universal is FALSE at
   B = 7, n = 8 (7^8 = 5,764,801 > 2^21 = 2,097,152; computed in the leg).

LEG INVENTORY (D7@2026-08-08, APPEND-AND-RECORD): _result() compares the
executed leg set against EXPECTED_LEGS set-exactly on the path the bank
would execute; a mismatch contributes a failure reason and does not raise.
STANDING LIMIT, disclosed: this certifies that a declared leg EXECUTED,
not that it COULD HAVE FAILED.

MAY-NOT-CITE (the frozen surface's list, binding here, carried verbatim):
- Not any supply claim -- "occupancy supplies the class" is stated nowhere
  and may not be inferred from K3's inhabitation.
- Not any identification of the constructed character with the measured
  class (the S4 genre; K5(c) exists to bar it).
- Not as evidence for or against situational-S -- the hypothesis stands
  whatever these type facts say.
- Not any frustration<->exit identification (magnitude-conditional
  corpus-wide).
- Not the join network for supply (its own MAY-NOT-CITE binds; it is cited
  here for the datum's TYPE only).
- Not K4 as outcome (2) or as "no occupancy supplier exists" -- the
  obstruction is construction-scoped (single-event, vertex-mediated,
  fixed-budget), not universal; the dissolution routes are named.
- Not K3 as passing the v2 gate -- an honest occupancy supplier cannot be
  presented to `eval_supply` at all, and class-only supply fails the
  full-datum bar structurally.
- The L7 negatives only in containment form; outcome (2) only from the
  decision doc's fixed final form.
This module describes what it COMPUTES.  Identity-level legs, records and
named imports are disclosed as such in the returned records.
"""

import ast
import sys
from itertools import combinations, permutations, product

HELD_OUT_OF_THE_BANK = False  # lifted by Ethan's ruling 2026-08-12; banked v24.3.472

CLAIM_SURFACE_SHA256 = (
    "0744de9bd8cbe925f3438a9325993055f1896cf795e2a27456d2b775700bf8e2")

# Named unforced imports.  Each is CONSUMED AS A NAME at the legs that need
# it; none is constructed, derived, or selected by anything computed here.
NAMED_IMPORTS = (
    # anchor universe <-> per-distinction realizations of the sep(P) ground
    # set.  The QAC's tie vocabulary (anchor tokens ('A', i)) and the sep
    # vocabulary (integers 0..n-1 under a partition P) are different index
    # sets with no banked map between them; K5(a) executes both and
    # constructs no map.
    "IOTA_anchor_universe_to_ground_set_identification",
    # an edge label reads only the two endpoint membership bits.  The
    # symmetric-Boolean-rule space K2 classifies is defined BY this import;
    # rules reading >= 3 vertices are not classified, and neither are the
    # 8 asymmetric two-bit tables (an asymmetric rule presupposes an edge
    # orientation no import supplies) -- stated domain bounds.
    "ENDPOINT_LOCALITY_factorization",
    # the global Z2 exchanging a situational rule with its complement
    # (AND <-> NAND).  It changes the class-map pointwise wherever the
    # antibalanced character is non-trivial and is fixed by nothing
    # computed in this module.
    "ANTIBALANCED_TWIST_convention",
)

# Named load-bearing standard-mathematics import (the
# continuation_join_network NAMED_MATH_IMPORTS style: recorded
# machine-readably, consumed if cited beyond the executed n, NOT
# derived here).  No leg's verdict consumes it -- every K1 leg is
# exhaustive at its stated n.
NAMED_MATH_IMPORTS = (
    # a coboundary (vertex-potential / switching-function) edge labeling
    # is balanced: trivial holonomy on every cycle.  Classical
    # signed-graph switching theory; K1 claims no novelty for the
    # identity it exhibits.
    "ZASLAVSKY_1982_SIGNED_GRAPHS_coboundary_labelings_have_trivial_holonomy",
)

# The only apf modules this module consumes; K5(c) enforces this set-exactly
# by AST scan of this module's own source.
DECLARED_APF_IMPORTS = (
    "apf.continuation_join_network",
    "apf.nonlocal_tie_resolution",
)

EXPECTED_LEGS = {
    "check_K1_coboundary_kill": [
        "census_69_connected_enforced",
        "cycle_space_even_degree_everywhere",
        "every_potential_trivial_on_whole_cycle_space",
        "natural_parity_supplies_only_the_balanced_endpoint",
        "xor_of_membership_is_a_vertex_potential",
    ],
    "check_K2_rule_collapse": [
        "eight_symmetric_rules_derived_not_stipulated",
        "exactly_one_situational_family_up_to_twist",
        "four_class_map_families_exhaustive",
        "twist_changes_the_class_exactly_on_nonbipartite",
        "twist_involution_is_a_named_convention_import",
    ],
    "check_K3_inhabitation_type_facts": [
        "class_valued_two_basis_identity",
        "endpoint_locality_and_iota_named_at_site",
        "r1_two_classes_wherever_dim_geq_1",
        "r6_non_endpoint_wherever_dim_geq_2",
        "sn_equivariance_label_level_n3_n4",
        "surjective_n_leq_4_and_dim_leq_3_at_n5",
        "switching_class_value_tie_j3_and_union_find",
    ],
    "check_K4_range_obstruction": [
        "class_side_confirmation_union_find",
        "exact_inequality_table_and_permanence",
        "full_range_failure_every_dim_geq_4",
        "image_factors_through_the_trace_bound",
        "n5_census_split_enforced",
        "obstruction_scope_and_dissolution_routes",
    ],
    "check_K5_import_controls": [
        "a_no_anchor_to_ground_set_map",
        "b_twist_and_endpoint_locality_controls",
        "c_no_represented_side_import_set_exact",
        "d_magnitude_non_supply_and_v2_gate_records",
    ],
}


# ---------------------------------------------------------------------------
# the census and the rules (codomain machinery consumed from the join
# network by import inside each check; helpers here are domain-side only)
# ---------------------------------------------------------------------------

def _census():
    """All connected sep graphs at n = 3, 4, 5 (every >= 2-block set
    partition).  Returns (graphs, per_n) with graphs a list of (n, P, E)."""
    from apf.continuation_join_network import _sep_edges, _set_partitions

    graphs = []
    per_n = {}
    for n in (3, 4, 5):
        cnt = 0
        for P in _set_partitions(n):
            if len(P) < 2:
                continue
            E = _sep_edges(P, n)
            graphs.append((n, tuple(tuple(sorted(b)) for b in P), E))
            cnt += 1
        per_n[n] = cnt
    return graphs, per_n


def _rule_and(u, v):
    """The membership-AND rule: the edge is -1 iff both endpoints are in X."""
    return -1 if (u and v) else 1


def _rule_xor(u, v):
    """The XOR-of-membership rule (the 'natural parity' reading)."""
    return -1 if (u ^ v) else 1


def _rule_nand(u, v):
    """The antibalanced twist of the membership-AND rule."""
    return 1 if (u and v) else -1


def _memb_labels(E, idx, memb, rule):
    """Edge labels in edge-index order from the endpoint membership bits.
    ENDPOINT_LOCALITY is the import consumed here: the rule reads exactly
    (memb[i], memb[j]) and nothing else."""
    lab = [0] * len(E)
    for (i, j) in E:
        lab[idx[(i, j)]] = rule(memb[i], memb[j])
    return tuple(lab)


def _potential_labels(E, idx, chi):
    """Edge labels of the vertex-potential (coboundary) genre:
    s_ij = chi(i) * chi(j)."""
    lab = [0] * len(E)
    for (i, j) in E:
        lab[idx[(i, j)]] = chi[i] * chi[j]
    return tuple(lab)


def _cycle_space(basis):
    """All 2^dim cycle-space elements as frozensets of edges (GF(2) spans
    of the fundamental-cycle basis)."""
    elems = []
    for mask in product((0, 1), repeat=len(basis)):
        acc = frozenset()
        for bit, c in zip(mask, basis):
            if bit:
                acc = acc ^ frozenset(c)
        elems.append(acc)
    return elems


def _fundamental_cycles_alt(verts, edges):
    """A SECOND fundamental-cycle basis (reverse-order BFS forest) for the
    basis-independence leg.  Deliberately a re-implementation: K3 compares
    the partition of X-space it induces against the one induced by the
    imported join-network basis."""
    adj = {v: [] for v in verts}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    parent = {}
    depth = {}
    tree = set()
    for root in sorted(verts, reverse=True):
        if root in depth:
            continue
        depth[root] = 0
        parent[root] = None
        queue = [root]
        for u in queue:
            for v in sorted(adj[u], reverse=True):
                if v not in depth:
                    depth[v] = depth[u] + 1
                    parent[v] = u
                    tree.add((u, v) if u < v else (v, u))
                    queue.append(v)

    def path_edges(x):
        out = set()
        while parent[x] is not None:
            p = parent[x]
            out.add((x, p) if x < p else (p, x))
            x = p
        return out

    cycles = []
    for e in edges:
        if e in tree:
            continue
        a, b = e
        sym = path_edges(a) ^ path_edges(b)
        cycles.append(tuple(sorted(sym | {e})))
    return cycles


def _kn_classes(n):
    """Exact switching-class count of K_n: 2^(m - n + 1)."""
    return 2 ** (n * (n - 1) // 2 - n + 1)


# ---------------------------------------------------------------------------
# result plumbing (append-and-record leg inventory)
# ---------------------------------------------------------------------------

def _result(name, legs, key_result, dependencies=(), cross_refs=(),
            disclosures=()):
    fails = []
    have = tuple(sorted(legs))
    want = tuple(EXPECTED_LEGS[name])
    if have != want:
        missing = sorted(set(want) - set(have))
        extra = sorted(set(have) - set(want))
        fails.append(
            f"leg inventory mismatch: missing={missing} extra={extra}")
    for label in sorted(legs):
        ok, ev = legs[label]
        if not ok:
            fails.append(f"{label}: {ev}")
    return {
        "name": name,
        "passed": not fails,
        "tier": 3,
        "epistemic": "P_math",
        "legs": {k: {"passed": bool(v[0]), "evidence": v[1]}
                 for k, v in legs.items()},
        "leg_count": len(legs),
        "fail_reasons": fails,
        "key_result": key_result,
        "conditional_on": [],
        "dependencies": list(dependencies),
        "cross_refs": list(cross_refs),
        "disclosures": list(disclosures),
        "named_imports": list(NAMED_IMPORTS),
        "named_math_imports": list(NAMED_MATH_IMPORTS),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "frozen_claim_surface_sha256": CLAIM_SURFACE_SHA256,
        "inventory_note": (
            "append-and-record (D7@2026-08-08): certifies a declared leg "
            "EXECUTED, not that it could have failed"),
    }


# ---------------------------------------------------------------------------
# K1 -- the coboundary kill
# ---------------------------------------------------------------------------

def check_K1_coboundary_kill():
    """K1: every vertex-potential edge labeling (covering every
    per-vertex function of occupancy data) has the trivial holonomy
    character on every realizable sep(P) at n <= 5 -- a theorem of the
    coboundary identity exhibited across the whole cycle space, all
    potentials, all 69 graphs.  The natural-parity (XOR) reading is a
    vertex-potential instance and supplies only the balanced endpoint."""
    from apf.continuation_join_network import (_bell, _components,
                                               _fundamental_cycles,
                                               holonomy_character)

    legs = {}
    graphs, per_n = _census()
    bell_expect = {n: _bell(n) - 1 for n in (3, 4, 5)}
    conn_ok = all(
        _components(list(range(n)), E) == 1 for (n, _P, E) in graphs)
    legs["census_69_connected_enforced"] = (
        len(graphs) == 69 and per_n == bell_expect
        and per_n == {3: 4, 4: 14, 5: 51} and conn_ok,
        {"graphs": len(graphs), "per_n": per_n,
         "bell_minus_one": bell_expect,
         "note": "every >= 2-block set partition at n = 3, 4, 5; each sep "
                 "graph verified connected (the J1 fact, re-derived)"})

    # the coboundary identity's engine: every cycle-space element has
    # all-even vertex degrees; hence chi-products are chi(v)^even = 1
    even_ok = True
    elements_checked = 0
    pot_ok = True
    pot_evals = 0
    xor_ok = True
    xor_instance_ok = True
    xy_pairs = 0
    expected_elements = 0
    expected_pot = 0
    for (n, _P, E) in graphs:
        idx = {e: k for k, e in enumerate(E)}
        basis = _fundamental_cycles(list(range(n)), E)
        dim = len(basis)
        expected_elements += 2 ** dim
        expected_pot += 2 ** n
        space = _cycle_space(basis)
        for elem in space:
            elements_checked += 1
            deg = {}
            for (i, j) in elem:
                deg[i] = deg.get(i, 0) + 1
                deg[j] = deg.get(j, 0) + 1
            even_ok &= all(d % 2 == 0 for d in deg.values())
        triv = (1,) * dim
        for chis in product((1, -1), repeat=n):
            pot_evals += 1
            lab = _potential_labels(E, idx, chis)
            # trivial on the whole space, not only the basis
            for elem in space:
                h = 1
                for e in elem:
                    h *= lab[idx[e]]
                pot_ok &= (h == 1)
            pot_ok &= (holonomy_character(lab, idx, basis) == triv)
        for bits in product((0, 1), repeat=n):
            xy_pairs += 1
            memb = {i: bits[i] for i in range(n)}
            xor_lab = _memb_labels(E, idx, memb, _rule_xor)
            chi = tuple(-1 if bits[i] else 1 for i in range(n))
            xor_instance_ok &= (xor_lab == _potential_labels(E, idx, chi))
            xor_ok &= (holonomy_character(xor_lab, idx, basis) == triv)

    legs["cycle_space_even_degree_everywhere"] = (
        even_ok and elements_checked == expected_elements
        and elements_checked == 796,
        {"cycle_space_elements_checked": elements_checked,
         "note": "every GF(2) span element of every graph's fundamental "
                 "basis has all-even vertex degrees -- the engine of the "
                 "coboundary identity, exhibited across the class"})
    legs["every_potential_trivial_on_whole_cycle_space"] = (
        pot_ok and pot_evals == expected_pot and pot_evals == 1888,
        {"potentials_evaluated": pot_evals,
         "elements_per_potential": "the graph's full 2^dim cycle space",
         "note": "all 2^n potentials chi -- covering every per-vertex "
                 "function of occupancy data -- give "
                 "chi(i)chi(j)-labelings with product 1 on every "
                 "cycle-space element and the trivial character"})
    legs["xor_of_membership_is_a_vertex_potential"] = (
        xor_instance_ok and xy_pairs == 1888,
        {"graph_X_pairs": xy_pairs,
         "instance": "XOR labels == potential labels with "
                     "chi(i) = (-1)^memb(i), exact tuple equality",
         "iota": "membership on the ground set is read under the named "
                 "import IOTA (see NAMED_IMPORTS); constructed nowhere"})
    legs["natural_parity_supplies_only_the_balanced_endpoint"] = (
        xor_ok and xy_pairs == 1888,
        {"graph_X_pairs": xy_pairs,
         "note": "the natural-parity reading's character is trivial (the "
                 "balanced endpoint) for every X on every graph"})

    return _result(
        "check_K1_coboundary_kill", legs,
        key_result=(
            f"The coboundary kill: on all {len(graphs)} connected sep "
            f"graphs at n = 3..5, every vertex-potential labeling (all "
            f"{pot_evals} potentials, covering every per-vertex function "
            f"of occupancy data) has product 1 on every one of the "
            f"{elements_checked} cycle-space elements and the trivial "
            f"holonomy character; the natural-parity (XOR-of-membership) "
            f"reading is a vertex-potential instance and supplies only the "
            f"balanced endpoint, for every X ({xy_pairs} (graph, X) "
            f"pairs).  A theorem of the coboundary identity exhibited "
            f"across the class, under the named import iota."),
        cross_refs=["continuation_join_network"],
        disclosures=[
            "codomain machinery (fundamental cycles, holonomy characters) "
            "is consumed from continuation_join_network by import, not "
            "re-implemented",
            "classical provenance: the coboundary-triviality identity is "
            "standard signed-graph switching theory -- the NAMED "
            "standard-mathematics import in NAMED_MATH_IMPORTS (Zaslavsky "
            "genre); no novelty is claimed, and no leg's verdict consumes "
            "the general statement (every leg is exhaustive at its "
            "stated n)",
            "scope bound: exhaustive at stated n (3..5) only"])


# ---------------------------------------------------------------------------
# K2 -- the rule collapse
# ---------------------------------------------------------------------------

def check_K2_rule_collapse():
    """K2: the eight symmetric Boolean endpoint rules (derived, not
    stipulated) collapse to four class-map families; exactly one
    situational family exists up to the antibalanced involution; the
    involution is a named convention import."""
    from apf.continuation_join_network import (_fundamental_cycles,
                                               holonomy_character)

    legs = {}
    graphs, _per_n = _census()

    # derive the 8 symmetric rules from all 16 Boolean functions of 2 bits
    named_tables = {
        "const+": (0, 0, 0, 0), "XOR": (0, 1, 1, 0), "AND": (0, 0, 0, 1),
        "OR": (0, 1, 1, 1), "const-": (1, 1, 1, 1), "XNOR": (1, 0, 0, 1),
        "NAND": (1, 1, 1, 0), "NOR": (1, 0, 0, 0)}
    all_tables = list(product((0, 1), repeat=4))  # (f00, f01, f10, f11)
    symmetric = [t for t in all_tables if t[1] == t[2]]
    derived_ok = (len(all_tables) == 16 and len(symmetric) == 8
                  and sorted(symmetric) == sorted(named_tables.values()))
    # rules built FROM the derived tables; the module-level _rule_and /
    # _rule_xor / _rule_nand are verified against them on all 4 inputs
    def _mk(table):
        return lambda u, v: -1 if table[2 * u + v] else 1
    rules = {nm: _mk(t) for nm, t in named_tables.items()}
    inst_ok = all(
        rules["AND"](u, v) == _rule_and(u, v)
        and rules["XOR"](u, v) == _rule_xor(u, v)
        and rules["NAND"](u, v) == _rule_nand(u, v)
        for u, v in product((0, 1), repeat=2))
    legs["eight_symmetric_rules_derived_not_stipulated"] = (
        derived_ok and inst_ok,
        {"boolean_functions_of_two_bits": len(all_tables),
         "symmetric": len(symmetric),
         "note": "the rule space is derived by symmetry-filtering all 16 "
                 "truth tables; the module-level AND/XOR/NAND rule "
                 "functions are verified against the derived tables on "
                 "all 4 inputs.  ENDPOINT_LOCALITY (see NAMED_IMPORTS) is "
                 "the import defining this rule space; rules reading >= 3 "
                 "vertices are not classified, and neither are the 8 "
                 "asymmetric two-bit tables -- a stated domain bound, not "
                 "a theorem computed here (an asymmetric rule presupposes "
                 "an edge orientation no import supplies)"})

    # exhaustive family collapse + fingerprints
    fam_ok = True
    evals = 0
    fingerprints = {nm: [] for nm in named_tables}
    varies_and = set()
    nonbip_anti = set()
    nonbip_blocks = set()
    twist_pointwise = 0
    bip_neutral = 0
    per_graph_and_const = {}
    for gi, (n, P, E) in enumerate(graphs):
        idx = {e: k for k, e in enumerate(E)}
        basis = _fundamental_cycles(list(range(n)), E)
        dim = len(basis)
        triv = (1,) * dim
        anti = holonomy_character((-1,) * len(E), idx, basis)
        if anti != triv:
            nonbip_anti.add(gi)
        if len(P) >= 3:
            nonbip_blocks.add(gi)
        # antibalanced non-trivial <=> some basis cycle of odd length
        odd_basis = any(len(c) % 2 == 1 for c in basis)
        fam_ok &= (odd_basis == (anti != triv))
        and_chars = set()
        for bits in product((0, 1), repeat=n):
            memb = {i: bits[i] for i in range(n)}
            chars = {}
            for nm, rule in rules.items():
                chars[nm] = holonomy_character(
                    _memb_labels(E, idx, memb, rule), idx, basis)
                fingerprints[nm].append(chars[nm])
            evals += 8
            fam_ok &= (chars["const+"] == triv and chars["XOR"] == triv)
            fam_ok &= (chars["const-"] == anti and chars["XNOR"] == anti)
            fam_ok &= (chars["OR"] == chars["AND"])
            twisted = tuple(a * b for a, b in zip(chars["AND"], anti))
            fam_ok &= (chars["NAND"] == twisted
                       and chars["NOR"] == chars["NAND"])
            and_chars.add(chars["AND"])
            if anti != triv:
                fam_ok &= (chars["NAND"] != chars["AND"])
                twist_pointwise += 1
            else:
                fam_ok &= (chars["NAND"] == chars["AND"])
                bip_neutral += 1
        if len(and_chars) >= 2:
            varies_and.add(gi)
        per_graph_and_const[gi] = (len(and_chars) == 1)
    legs["four_class_map_families_exhaustive"] = (
        fam_ok and evals == 8 * 1888,
        {"rule_evaluations": evals,
         "identities": "const+ = XOR = trivial; const- = XNOR = "
                       "antibalanced; OR = AND; NOR = NAND = "
                       "AND * antibalanced -- per (graph, X), exhaustive",
         "antibalanced_criterion": "non-trivial <=> an odd-length basis "
                                   "cycle exists (verified per graph)"})

    # family grouping and the situational count
    fps = {nm: tuple(fp) for nm, fp in fingerprints.items()}
    groups = {}
    for nm, fp in fps.items():
        groups.setdefault(fp, set()).add(nm)
    families = sorted(groups.values(), key=lambda s: sorted(s))
    want_families = [{"AND", "OR"}, {"NAND", "NOR"},
                     {"XNOR", "const-"}, {"XOR", "const+"}]
    grouping_ok = (len(families) == 4
                   and sorted(map(sorted, families))
                   == sorted(map(sorted, want_families)))
    # X-dependence: the AND family varies on every dim >= 1 graph and on
    # no tree; endpoint families are constant-in-X everywhere
    dims = {}
    from apf.continuation_join_network import _fundamental_cycles as _fc
    for gi, (n, _P, E) in enumerate(graphs):
        dims[gi] = len(_fc(list(range(n)), E))
    dim_ge1 = {gi for gi, d in dims.items() if d >= 1}
    situational_ok = (varies_and == dim_ge1 and len(dim_ge1) == 57
                      and all(per_graph_and_const[gi]
                              for gi in dims if dims[gi] == 0))
    # the twist pairs the four families into two orbits
    def _twistfp(nm_from):
        out = []
        k = 0
        for gi, (n, _P, E) in enumerate(graphs):
            idx = {e: kk for kk, e in enumerate(E)}
            basis = _fc(list(range(n)), E)
            anti = holonomy_character((-1,) * len(E), idx, basis)
            for _bits in range(2 ** n):
                out.append(tuple(a * b for a, b in
                                 zip(fps[nm_from][k], anti)))
                k += 1
        return tuple(out)
    partners = {"AND": "NAND", "NAND": "AND", "OR": "NOR", "NOR": "OR",
                "const+": "const-", "const-": "const+",
                "XOR": "XNOR", "XNOR": "XOR"}
    twist_all_ok = all(_twistfp(nm) == fps[partners[nm]]
                       for nm in sorted(partners))
    pairing_ok = (twist_all_ok
                  and _twistfp("AND") == fps["NAND"]
                  and _twistfp("NAND") == fps["AND"])
    legs["exactly_one_situational_family_up_to_twist"] = (
        grouping_ok and situational_ok and pairing_ok,
        {"families": [sorted(s) for s in families],
         "situational": "the {AND, OR} family varies with X on every "
                        "dim >= 1 graph (57 of 69, enforced) and on no "
                        "tree; both endpoint families are constant in X "
                        "on all 69",
         "twist_orbits": "the involution pairs {const+, XOR} <-> "
                         "{const-, XNOR} and {AND, OR} <-> {NAND, NOR}: "
                         "2 orbits, exactly 1 situational"})

    legs["twist_changes_the_class_exactly_on_nonbipartite"] = (
        nonbip_anti == nonbip_blocks and len(nonbip_anti) == 44
        and len(graphs) - len(nonbip_anti) == 25
        and twist_pointwise == 1272 and bip_neutral == 616
        and twist_pointwise + bip_neutral == 1888,
        {"nonbipartite_graphs": len(nonbip_anti),
         "bipartite_graphs": len(graphs) - len(nonbip_anti),
         "criterion_match": "antibalanced-nontrivial set == the >= "
                            "3-block set (both computed)",
         "pointwise_changes": twist_pointwise,
         "class_neutral_evaluations": bip_neutral,
         "weakening": "the frozen 'changes the class' is carried in "
                      "computed form: the twist changes the class-map "
                      "POINTWISE at every X on exactly the 44 "
                      "non-bipartite graphs and is class-neutral on the "
                      "25 bipartite ones"})
    legs["twist_involution_is_a_named_convention_import"] = (
        twist_all_ok and len(partners) == 8,
        {"import": "ANTIBALANCED_TWIST_convention (see NAMED_IMPORTS)",
         "computed_content": "applying the twist maps each of the 8 rule "
                             "fingerprints to its partner's (all 8 "
                             "transports executed), so twice is the "
                             "identity on every fingerprint; which member "
                             "of the {AND, OR} / {NAND, NOR} pair obtains "
                             "is fixed by nothing computed in this module "
                             "-- a named unforced Z2 import"})

    return _result(
        "check_K2_rule_collapse", legs,
        key_result=(
            f"The rule collapse: the {len(symmetric)} symmetric Boolean "
            f"endpoint rules (derived from all {len(all_tables)} "
            f"two-bit functions) fall into exactly {len(families)} "
            f"class-map families over all {evals} rule evaluations "
            f"(69 graphs x all X x 8 rules); the antibalanced involution "
            f"pairs them into 2 orbits of which exactly 1 is situational "
            f"(X-dependent on all {len(dim_ge1)} dim >= 1 graphs).  The "
            f"involution is a NAMED Z2 convention import; it changes the "
            f"class-map pointwise on exactly the {len(nonbip_anti)} "
            f"non-bipartite graphs and is class-neutral on the "
            f"{len(graphs) - len(nonbip_anti)} bipartite ones."),
        cross_refs=["continuation_join_network"],
        disclosures=[
            "WEAKENING (permitted direction): the frozen 'the involution "
            "... changes the class' is carried as the computed pointwise "
            "statement above; as SETS the AND and NAND images coincide on "
            "all 69 graphs at stated n (see K5(b))",
            "scope bound: the rule space classified is the symmetric "
            "Boolean ENDPOINT rules (the ENDPOINT_LOCALITY import); rules "
            "reading >= 3 vertices are not classified, and neither are "
            "the 8 asymmetric two-bit tables (a stated domain bound: an "
            "asymmetric rule presupposes an edge orientation no import "
            "supplies; nothing computed here classifies them)"])


# ---------------------------------------------------------------------------
# K3 -- the inhabitation type facts
# ---------------------------------------------------------------------------

def check_K3_inhabitation_type_facts():
    """K3: type facts of the membership-AND map -- equivariance,
    class-valuedness/basis-freeness, R1, R6, and surjectivity at n <= 4
    and dim <= 3 at n = 5 -- stated as TYPE FACTS about a constructed toy
    map under two named imports (iota, endpoint-locality), never as a
    reading of the world."""
    from apf.continuation_join_network import (
        _fundamental_cycles, _sep_edges, _set_partitions,
        _switching_classes, check_J3_class_character_bijection,
        holonomy_character)

    legs = {}
    graphs, _per_n = _census()

    # (1) S_n-equivariance, label level, n = 3, 4, exhaustive
    eq_ok = True
    eq_count = 0
    for n in (3, 4):
        for P in _set_partitions(n):
            if len(P) < 2:
                continue
            E = _sep_edges(P, n)
            idx = {e: k for k, e in enumerate(E)}
            for bits in product((0, 1), repeat=n):
                memb = {i: bits[i] for i in range(n)}
                lab = _memb_labels(E, idx, memb, _rule_and)
                signs = {e: lab[idx[e]] for e in E}
                for pi in permutations(range(n)):
                    Ppi = [sorted(pi[x] for x in b) for b in P]
                    Epi = _sep_edges(Ppi, n)
                    idx_pi = {e: k for k, e in enumerate(Epi)}
                    memb_pi = {pi[i]: bits[i] for i in range(n)}
                    lab_pi = _memb_labels(Epi, idx_pi, memb_pi, _rule_and)
                    transported = {
                        (min(pi[a], pi[b]), max(pi[a], pi[b])): s
                        for (a, b), s in signs.items()}
                    eq_ok &= (
                        sorted(Epi) == sorted(transported)
                        and all(lab_pi[idx_pi[e]] == transported[e]
                                for e in Epi))
                    eq_count += 1
    legs["sn_equivariance_label_level_n3_n4"] = (
        eq_ok and eq_count == 5568,
        {"transport_identities": eq_count,
         "note": "192 at n = 3 (4 partitions x 8 X x 6 permutations) + "
                 "5376 at n = 4 (14 x 16 x 24), label-level exact, hence "
                 "class-level"})

    # (2) class-valued / basis-free: two-basis partition identity
    basis_ok = True
    bases_differ = 0
    for (n, _P, E) in graphs:
        verts = list(range(n))
        b1 = _fundamental_cycles(verts, E)
        b2 = _fundamental_cycles_alt(verts, E)
        if sorted(b1) != sorted(b2):
            bases_differ += 1
        idx = {e: k for k, e in enumerate(E)}
        part1 = {}
        part2 = {}
        for bits in product((0, 1), repeat=n):
            memb = {i: bits[i] for i in range(n)}
            lab = _memb_labels(E, idx, memb, _rule_and)
            part1.setdefault(
                holonomy_character(lab, idx, b1), set()).add(bits)
            part2.setdefault(
                holonomy_character(lab, idx, b2), set()).add(bits)
        basis_ok &= (sorted(map(sorted, part1.values()))
                     == sorted(map(sorted, part2.values())))
    legs["class_valued_two_basis_identity"] = (
        basis_ok and bases_differ == 51,
        {"graphs": len(graphs), "bases_genuinely_differ_on": bases_differ,
         "note": "the imported join-network basis vs an independent "
                 "reverse-order BFS basis induce IDENTICAL partitions of "
                 "X-space on all 69 graphs; the anti-vacuity count (51 "
                 "graphs where the bases differ as sets) is enforced"})

    # (3) R1 and R6 and the dim census
    dim0 = dim1 = dimge2 = 0
    r1_ok = True
    r6_ok = True
    images = {}
    for gi, (n, _P, E) in enumerate(graphs):
        idx = {e: k for k, e in enumerate(E)}
        basis = _fundamental_cycles(list(range(n)), E)
        dim = len(basis)
        if dim == 0:
            dim0 += 1
        elif dim == 1:
            dim1 += 1
        else:
            dimge2 += 1
        triv = (1,) * dim
        anti = holonomy_character((-1,) * len(E), idx, basis)
        img = set()
        for bits in product((0, 1), repeat=n):
            memb = {i: bits[i] for i in range(n)}
            img.add(holonomy_character(
                _memb_labels(E, idx, memb, _rule_and), idx, basis))
        images[gi] = (n, dim, img, triv, anti)
        if dim >= 1:
            r1_ok &= (len(img) >= 2)
        else:
            r1_ok &= (len(img) == 1)
        if dim >= 2:
            r6_ok &= (len(img - {triv, anti}) >= 1)
    census_ok = (dim0 == 12 and dim1 == 4 and dimge2 == 53
                 and dim0 + dim1 + dimge2 == 69)
    legs["r1_two_classes_wherever_dim_geq_1"] = (
        r1_ok and census_ok,
        {"dim_geq_1_graphs": dim1 + dimge2, "trees": dim0,
         "note": "two X over the same P land in different classes on "
                 "every dim >= 1 graph (57, enforced); trees carry one "
                 "class (their cycle space is trivial)"})
    legs["r6_non_endpoint_wherever_dim_geq_2"] = (
        r6_ok and dimge2 == 53,
        {"dim_geq_2_graphs": dimge2,
         "note": "a class outside {balanced, antibalanced} is attained on "
                 "every dim >= 2 graph -- the R6 presupposition met at "
                 "the audit's stated boundary"})

    # (4) surjectivity at n <= 4 and dim <= 3 at n = 5, in genuine
    # switching-class terms (union-find over the actual action, imported)
    surj_ok = True
    tie_ok = True
    surj_graphs = 0
    for gi, (n, dim, img, _t, _a) in images.items():
        if not (n <= 4 or dim <= 3):
            continue
        surj_graphs += 1
        surj_ok &= (len(img) == 2 ** dim)
        _n, _P, E = graphs[gi]
        _pats, idx, classes = _switching_classes(E, range(n))
        basis = _fundamental_cycles(list(range(n)), E)
        tie_ok &= (len(classes) == 2 ** dim)
        chars = []
        for cls in classes:
            cs = {holonomy_character(p, idx, basis) for p in cls}
            tie_ok &= (len(cs) == 1)
            chars.append(next(iter(cs)))
        tie_ok &= (len(set(chars)) == len(chars))
        tie_ok &= (img == set(chars))
    legs["surjective_n_leq_4_and_dim_leq_3_at_n5"] = (
        surj_ok and surj_graphs == 43,
        {"graphs": surj_graphs,
         "note": "18 graphs at n <= 4 plus 25 dim <= 3 graphs at n = 5; "
                 "image cardinality == 2^dim on each"})

    r_j3 = check_J3_class_character_bijection()
    ext = r_j3["legs"]["extension_complete_multipartite_n4_n5"]["evidence"]
    legs["switching_class_value_tie_j3_and_union_find"] = (
        tie_ok and r_j3.get("passed") is True
        and ext.get("graphs") == {"4": 14, "5": 51},
        {"banked_tie": "check_J3_class_character_bijection executed, "
                       "passed, its extension rows {4: 14, 5: 51} "
                       "consumed (the class <-> character bijection on "
                       "every sep graph at n = 4, 5)",
         "own_union_find": "on each of the 43 surjective-family graphs, "
                           "switching classes recomputed via the imported "
                           "_switching_classes; class count == 2^dim, one "
                           "character per class, all distinct, and the "
                           "AND image IS the full character set -- "
                           "surjectivity verified in class terms, not "
                           "only character terms"})

    # (5) the imports, named at site + the endpoint-locality witness
    loc_ok = True
    loc_count = 0
    expected_loc = 0
    for (n, _P, E) in graphs:
        idx = {e: k for k, e in enumerate(E)}
        expected_loc += len(E) * 2 ** n
        for bits in product((0, 1), repeat=n):
            memb = {i: bits[i] for i in range(n)}
            lab = _memb_labels(E, idx, memb, _rule_and)
            for (i, j) in E:
                w = min(v for v in range(n) if v not in (i, j))
                flipped = dict(memb)
                flipped[w] = 1 - flipped[w]
                lab_f = _memb_labels(E, idx, flipped, _rule_and)
                loc_ok &= (lab_f[idx[(i, j)]] == lab[idx[(i, j)]])
                loc_count += 1
    legs["endpoint_locality_and_iota_named_at_site"] = (
        loc_ok and loc_count == expected_loc and loc_count == 12872,
        {"third_vertex_flip_tests": loc_count,
         "computed_content": "the label at (i, j) is unchanged by "
                             "flipping membership at any third vertex "
                             "(executed witness of the endpoint-locality "
                             "factorization)",
         "imports_named": ["IOTA_anchor_universe_to_ground_set_"
                           "identification (X read as a ground-set "
                           "subset only under iota; constructed nowhere)",
                           "ENDPOINT_LOCALITY_factorization (the rule "
                           "reads exactly the two endpoint bits)"]})

    return _result(
        "check_K3_inhabitation_type_facts", legs,
        key_result=(
            f"Inhabitation TYPE FACTS of the membership-AND map, under "
            f"two named imports (iota, endpoint-locality): "
            f"S_n-equivariant ({eq_count} label-level transport "
            f"identities at n = 3, 4, exhaustive); class-valued and "
            f"cycle-basis-free (two-basis partition identity on all "
            f"{len(graphs)} graphs, bases differing on {bases_differ}); "
            f"two classes over one P on every dim >= 1 graph "
            f"({dim1 + dimge2}); a non-endpoint class on every dim >= 2 "
            f"graph ({dimge2}); surjective onto all 2^dim switching "
            f"classes on all {surj_graphs} graphs with n <= 4 or "
            f"dim <= 3 at n = 5, verified in genuine class terms.  These "
            f"are facts about a CONSTRUCTED TOY MAP -- never a reading "
            f"of the world, and never a supply claim."),
        dependencies=["J3_class_character_bijection"],
        cross_refs=["continuation_join_network"],
        disclosures=[
            "TYPE FACTS ONLY: nothing here states or implies 'occupancy "
            "supplies the class' (MAY-NOT-CITE, carried); the "
            "identification obligation is untouched",
            "scope bound: exhaustive at stated n; equivariance executed "
            "at n = 3, 4 only"])


# ---------------------------------------------------------------------------
# K4 -- the range obstruction
# ---------------------------------------------------------------------------

def check_K4_range_obstruction():
    """K4: the executed full-range failure at every n = 5 sep(P) with
    cyclomatic >= 4 (images 14/16, 20/32, 22/64, exact, class-side
    confirmed), and the cardinality certificate for suppliers factoring
    through B-valued per-vertex traces at fixed B = 2..64 (exact
    arithmetic; the per-B threshold n_B is sufficient, not minimal --
    the first-fail table carries the true minima for B = 2..6).  AN
    OBSTRUCTION
    CERTIFICATE ABOUT A CANDIDATE FAMILY (single-event, vertex-mediated,
    fixed per-vertex budget) -- NOT about all possible suppliers."""
    from apf.continuation_join_network import (_fundamental_cycles,
                                               _switching_classes,
                                               holonomy_character)
    from apf.nonlocal_tie_resolution import _local_tie

    legs = {}
    graphs, _per_n = _census()
    n5 = [(n, P, E) for (n, P, E) in graphs if n == 5]

    # (1) the n = 5 census split
    dim_counts = {}
    dims = {}
    for gi, (n, _P, E) in enumerate(n5):
        d = len(_fundamental_cycles(list(range(n)), E))
        dims[gi] = d
        dim_counts[d] = dim_counts.get(d, 0) + 1
    split_ok = (len(n5) == 51
                and dim_counts == {0: 5, 2: 10, 3: 10, 4: 15, 5: 10, 6: 1}
                and sum(c for d, c in dim_counts.items() if d >= 4) == 26
                and sum(c for d, c in dim_counts.items() if d <= 3) == 25)
    legs["n5_census_split_enforced"] = (
        split_ok,
        {"n5_graphs": len(n5), "by_dim": dim_counts,
         "obstructed_dim_geq_4": 26, "surjective_family_dim_leq_3": 25})

    # (2) full-range failure at every dim >= 4 graph, images exact
    pinned_img = {4: 14, 5: 20, 6: 22}
    fail_ok = True
    per_dim_graphs = {4: 0, 5: 0, 6: 0}
    images = {}
    for gi, (n, _P, E) in enumerate(n5):
        d = dims[gi]
        if d < 4:
            continue
        per_dim_graphs[d] += 1
        idx = {e: k for k, e in enumerate(E)}
        basis = _fundamental_cycles(list(range(n)), E)
        img = set()
        for bits in product((0, 1), repeat=n):
            memb = {i: bits[i] for i in range(n)}
            img.add(holonomy_character(
                _memb_labels(E, idx, memb, _rule_and), idx, basis))
        images[gi] = img
        fail_ok &= (len(img) == pinned_img[d] and 2 ** d > len(img))
    legs["full_range_failure_every_dim_geq_4"] = (
        fail_ok and per_dim_graphs == {4: 15, 5: 10, 6: 1},
        {"graphs_by_dim": per_dim_graphs,
         "images": {"dim 4": f"{pinned_img[4]} of {2 ** 4}",
                    "dim 5": f"{pinned_img[5]} of {2 ** 5}",
                    "dim 6": f"{pinned_img[6]} of {2 ** 6}"},
         "note": "image cardinality enforced per graph against the "
                 "frozen figures; uniform within each dim"})

    # (3) class-side confirmation on all 26 obstructed graphs
    cls_ok = True
    cls_graphs = 0
    for gi, (n, _P, E) in enumerate(n5):
        d = dims[gi]
        if d < 4:
            continue
        cls_graphs += 1
        _pats, idx, classes = _switching_classes(E, range(n))
        basis = _fundamental_cycles(list(range(n)), E)
        cls_ok &= (len(classes) == 2 ** d)
        chars = []
        for cls in classes:
            cs = {holonomy_character(p, idx, basis) for p in cls}
            cls_ok &= (len(cs) == 1)
            chars.append(next(iter(cs)))
        cls_ok &= (len(set(chars)) == 2 ** d)
        hit = sum(1 for ch in chars if ch in images[gi])
        cls_ok &= (hit == pinned_img[d] and hit == len(images[gi]))
    legs["class_side_confirmation_union_find"] = (
        cls_ok and cls_graphs == 26,
        {"obstructed_graphs_confirmed": cls_graphs,
         "note": "switching classes recomputed by union-find over the "
                 "actual action (imported); class count == 2^dim, one "
                 "character per class, all distinct; the image counted "
                 "in CLASSES equals the image counted in characters "
                 "(14/20/22)"})

    # (4) the factoring bound: image <= #labelings <= 2^n = B^n at B = 2
    fac_ok = True
    for gi, (n, _P, E) in enumerate(n5):
        idx = {e: k for k, e in enumerate(E)}
        labelings = set()
        for bits in product((0, 1), repeat=n):
            memb = {i: bits[i] for i in range(n)}
            labelings.add(_memb_labels(E, idx, memb, _rule_and))
        d = dims[gi]
        img_size = pinned_img[d] if d >= 4 else 2 ** d
        fac_ok &= (img_size <= len(labelings) <= 2 ** n)
    k5_forced = (2 ** 5 < 2 ** 6)
    legs["image_factors_through_the_trace_bound"] = (
        fac_ok and k5_forced and 2 ** 5 == 32 and 2 ** 6 == 64,
        {"chain": "|image| <= |{labelings}| <= 2^n = B^n at B = 2, "
                  "enforced on every n = 5 graph",
         "k5_boundary": f"at K5 the certificate alone forces failure: "
                        f"2^5 = {2 ** 5} < 2^(m-n+1) = {2 ** 6}; at "
                        f"dim 4 and dim 5 the failures (14 < 16, "
                        f"20 < 32) are EXECUTED facts beyond the "
                        f"counting bound"})

    # (5) the exact inequality table with permanence certificates
    first_fail = {}
    table_ok = True
    for B in range(2, 7):
        ff = None
        for n in range(3, 13):
            if B ** n < _kn_classes(n):
                ff = n
                break
        first_fail[B] = ff
    table_ok &= (first_fail == {2: 5, 3: 6, 4: 7, 5: 8, 6: 8})
    # permanence: base + step (classes(n+1) = classes(n) * 2^(n-1);
    # 2^(n-1) > B for all n >= n0 since 2^(n0-1) > B), executed to n = 12
    for B, n0 in first_fail.items():
        table_ok &= (2 ** (n0 - 1) > B)
        table_ok &= all(B ** n < _kn_classes(n) for n in range(n0, 13))
    step_ok = all(_kn_classes(n + 1) == _kn_classes(n) * 2 ** (n - 1)
                  for n in range(3, 13))
    # general-B certificate: for every fixed B in 2..64, failure from
    # the sufficient (not minimal) threshold n_B = 2*ceil(log2 B) + 4
    gen_ok = True
    for B in range(2, 65):
        c = (B - 1).bit_length()
        n_B = 2 * c + 4
        gen_ok &= (B <= 2 ** c)
        gen_ok &= (B ** n_B < _kn_classes(n_B))
        gen_ok &= (2 ** (n_B - 1) > B)
    # the weakening's reason, computed: the frozen universal fails at B = 7
    counterexample = (7 ** 8, _kn_classes(8))
    weak_ok = (counterexample[0] > counterexample[1]
               and counterexample == (5764801, 2097152))
    legs["exact_inequality_table_and_permanence"] = (
        table_ok and step_ok and gen_ok and weak_ok,
        {"first_fail_by_B": first_fail,
         "permanence": "per B: base at first-fail n0 plus the step "
                       "classes(n+1) = classes(n) * 2^(n-1) with "
                       "2^(n0-1) > B -- so failure holds for ALL "
                       "n >= n0 by induction (base and step executed "
                       "exactly; verified numerically through n = 12)",
         "general_B": "for every fixed B in 2..64, failure from the "
                      "SUFFICIENT threshold n_B = 2*ceil(log2 B) + 4 "
                      "(base, bound B <= 2^c, and step executed exactly "
                      "per B; not minimal -- the first_fail row has B = 2 "
                      "first failing at n = 5 while n_B(2) = 6)",
         "general_B_identity_note": (
             "NOT A LEG: the certificate's closing algebra "
             "c*(2c+4) < (2c+3)*(c+1), i.e. 0 < c + 3 in "
             "c = ceil(log2 B), is a one-line identity; it is recorded "
             "as an identity-level note only -- no leg executes B >= 65 "
             "and no returned verdict depends on it"),
         "weakening": f"the frozen 'from n = 8 at every fixed B' is "
                      f"FALSE as a universal: 7^8 = {counterexample[0]} "
                      f"> 2^21 = {counterexample[1]}; carried here as "
                      f"'every fixed B <= 6 from n = 8' plus the "
                      f"sufficient per-B threshold certificate for "
                      f"B = 2..64"})

    # (6) the scope of the obstruction, in computed form
    disjoint_ok = True
    for k in (1, 2, 3):
        A, Bopt = _local_tie(k)
        disjoint_ok &= (A & Bopt == frozenset() and len(A) == len(Bopt) == k)
    silent_B = 8
    silent = (silent_B ** 5 >= _kn_classes(5))
    legs["obstruction_scope_and_dissolution_routes"] = (
        disjoint_ok and silent and silent_B ** 5 == 32768,
        {"candidate_family": "suppliers factoring through B-valued "
                             "per-vertex occupancy traces at a FIXED "
                             "budget B, from a SINGLE-EVENT, "
                             "VERTEX-MEDIATED occupancy channel",
         "single_event_vertex_mediated_computed": (
             "the home module's tie options are DISJOINT by construction "
             "(nonlocal_tie_resolution._local_tie executed at k = 1, 2, "
             "3: A & B empty, equal sizes); no pairwise-shared count is "
             "computed here"),
         "certificate_is_silent_for_large_budgets": (
             f"computed: at n = 5 a budget B = {silent_B} gives "
             f"{silent_B}^5 = {silent_B ** 5} >= {_kn_classes(5)} -- the "
             f"counting bound does not bite there; NO supplier is "
             f"constructed and none is implied"),
         "dissolution_routes_named": [
             "a banked pairwise-shared-substrate realization supplying "
             "per-separated-pair join data (C6)",
             "a banked edge-indexed tie-event family (C5)",
             "a per-vertex budget growing with n as a DERIVED (not "
             "stipulated) schedule"],
         "route_status": "each is an import absent at HEAD; each "
                         "re-enters the S2 trichotomy at its own "
                         "sourcing"})

    return _result(
        "check_K4_range_obstruction", legs,
        key_result=(
            f"The range obstruction, construction-scoped: at n = 5 the "
            f"membership-AND map fails surjectivity on every sep(P) with "
            f"cyclomatic >= 4 -- images {pinned_img[4]} of {2 ** 4} on "
            f"all {per_dim_graphs[4]} dim-4 graphs, {pinned_img[5]} of "
            f"{2 ** 5} on all {per_dim_graphs[5]} dim-5 graphs, "
            f"{pinned_img[6]} of {2 ** 6} at K5 -- exact and class-side "
            f"confirmed; and any supplier factoring through B-valued "
            f"per-vertex occupancy traces has image <= B^n < 2^(m-n+1) "
            f"on K_n from n = {first_fail[2]} at B = 2 (executed "
            f"first-fail table, B = 2..6) and from the certified "
            f"sufficient threshold n_B = 2*ceil(log2 B) + 4 at every "
            f"fixed B in 2..64 (executed exactly; sufficient, not "
            f"minimal).  What is computed: the single-event, "
            f"vertex-mediated MEMBERSHIP reading fails from n = 5 "
            f"(executed), and every FIXED-BUDGET per-vertex trace "
            f"reading with B in 2..64 fails from the certified "
            f"sufficient threshold on K_n.  This is an obstruction "
            f"certificate about that CANDIDATE FAMILY -- not 'no "
            f"occupancy supplier exists'; the dissolution routes are "
            f"named in the leg record."),
        dependencies=["T_nonlocal_tie_resolution"],
        cross_refs=["continuation_join_network"],
        disclosures=[
            "SCOPE: the obstruction is construction-scoped "
            "(single-event, vertex-mediated, fixed-budget), not "
            "universal (MAY-NOT-CITE: not as outcome (2), not as 'no "
            "occupancy supplier exists')",
            "WEAKENING (permitted direction): the frozen 'from n = 8 at "
            "every fixed B' fails at B = 7, n = 8 (computed in the "
            "table leg); carried as B <= 6 from n = 8 plus the "
            "sufficient per-B threshold certificate for every fixed B "
            "in 2..64 (not minimal)"])


# ---------------------------------------------------------------------------
# K5 -- the import and non-identity controls (B4/J4 style, permanent)
# ---------------------------------------------------------------------------

# INHERITED RED (E1@2026-08-28: sub-lemma L_cost_C1 of check_L_cost
# demoted off 'P' to a POSTULATE).  THIS CHECK HOLDS NO VIEW ABOUT
# L_cost_C1: it reddens because its proximate anchor reddened, and that
# anchor is check_T_nonlocal_tie_resolution (nonlocal_tie_resolution.py).
# The leg that reads C1's status literal is in
# check_L_selection_ledger_completeness (born_at_ties.py); this red is
# inherited from it, and a reader who counts it as a separate finding
# over-counts the corpus's damage.
# NOT to be widened, tuned green, or reverted: the predicate is
# satisfiable and clears when C1 is discharged or the anchor's
# predicate is ruled.
def check_K5_import_controls():
    """K5: (a) no anchor-universe -> ground-set map constructed, with the
    home module's own join-count functions executed; (b) the twist and
    endpoint-locality named imports, with the AND/NAND control; (c) no
    represented-side import, set-exact; (d) magnitude non-supply computed
    at the output level and the v2-gate facts carried as records."""
    from apf.continuation_join_network import (_fundamental_cycles,
                                               holonomy_character)
    from apf.nonlocal_tie_resolution import (
        EPS, _deficit, _external, _joint, _local_tie,
        check_T_nonlocal_tie_resolution)

    legs = {}
    graphs, _per_n = _census()

    # (a) the two vocabularies, executed; no map constructed
    r_home = check_T_nonlocal_tie_resolution()
    grid = 0
    grid_ok = True
    token_ok = True
    for k in (1, 2, 3):
        A, B = _local_tie(k)
        for tok in A | B:
            token_ok &= (isinstance(tok, tuple) and len(tok) == 2
                         and isinstance(tok[0], str)
                         and isinstance(tok[1], int))
        for a in range(k + 1):
            for b in range(k + 1):
                for xo in range(3):
                    X = _external(A, B, a, b, xo)
                    grid_ok &= (_joint(A, X) - _joint(B, X)
                                == (b - a) * EPS)
                    grid_ok &= ((_deficit(A, X) > 0) == (len(A & X) > 0))
                    grid += 1
    ground_set_sample = set(range(5))
    A3, B3 = _local_tie(3)
    vocab_disjoint = ((A3 | B3) & ground_set_sample == set())
    legs["a_no_anchor_to_ground_set_map"] = (
        r_home.get("passed") is True and grid_ok and grid == 87
        and token_ok and vocab_disjoint,
        {"home_check": "T_nonlocal_tie_resolution executed, passed",
         "join_count_identity": f"jA - jB == (b - a)*eps re-executed "
                                f"through the home module's own "
                                f"_joint/_deficit over the full {grid}"
                                f"-case grid (its Leg-2 class)",
         "vocabularies": "anchor tokens are ('A'|'B'|'X', int) tuples; "
                         "the sep(P) ground set is integers 0..n-1; the "
                         "two index sets are disjoint (executed)",
         "control": "NO map between the QAC anchor universe and any "
                    "sep(P) ground set is constructed anywhere in this "
                    "module; every K1-K4 leg reads membership bits on "
                    "the ground set only under the NAMED import iota "
                    "(J4(c) carried)"})

    # (b) the twist control: AND and NAND both pass the type requirements
    # computed here, with pointwise-different class-maps off bipartite
    nand_eq_ok = True
    nand_eq_count = 0
    from apf.continuation_join_network import _sep_edges, _set_partitions
    n = 3
    for P in _set_partitions(n):
        if len(P) < 2:
            continue
        E = _sep_edges(P, n)
        idx = {e: k for k, e in enumerate(E)}
        for bits in product((0, 1), repeat=n):
            memb = {i: bits[i] for i in range(n)}
            lab = _memb_labels(E, idx, memb, _rule_nand)
            signs = {e: lab[idx[e]] for e in E}
            for pi in permutations(range(n)):
                Ppi = [sorted(pi[x] for x in b) for b in P]
                Epi = _sep_edges(Ppi, n)
                idx_pi = {e: k for k, e in enumerate(Epi)}
                memb_pi = {pi[i]: bits[i] for i in range(n)}
                lab_pi = _memb_labels(Epi, idx_pi, memb_pi, _rule_nand)
                transported = {
                    (min(pi[a], pi[b]), max(pi[a], pi[b])): s
                    for (a, b), s in signs.items()}
                nand_eq_ok &= all(lab_pi[idx_pi[e]] == transported[e]
                                  for e in Epi)
                nand_eq_count += 1
    nand_type_ok = True
    pointwise_diff = 0
    sets_coincide = 0
    for (nn, P, E) in graphs:
        verts = list(range(nn))
        idx = {e: k for k, e in enumerate(E)}
        b1 = _fundamental_cycles(verts, E)
        b2 = _fundamental_cycles_alt(verts, E)
        dim = len(b1)
        triv = (1,) * dim
        anti = holonomy_character((-1,) * len(E), idx, b1)
        part1 = {}
        part2 = {}
        img_and = set()
        img_nand = set()
        for bits in product((0, 1), repeat=nn):
            memb = {i: bits[i] for i in range(nn)}
            lab_n = _memb_labels(E, idx, memb, _rule_nand)
            lab_a = _memb_labels(E, idx, memb, _rule_and)
            ch_n = holonomy_character(lab_n, idx, b1)
            ch_a = holonomy_character(lab_a, idx, b1)
            part1.setdefault(ch_n, set()).add(bits)
            part2.setdefault(
                holonomy_character(lab_n, idx, b2), set()).add(bits)
            img_nand.add(ch_n)
            img_and.add(ch_a)
            if anti != triv:
                nand_type_ok &= (ch_n != ch_a)
                pointwise_diff += 1
        nand_type_ok &= (sorted(map(sorted, part1.values()))
                         == sorted(map(sorted, part2.values())))
        if dim >= 1:
            nand_type_ok &= (len(img_nand) >= 2)
        if dim >= 2:
            nand_type_ok &= (len(img_nand - {triv, anti}) >= 1)
        if img_and == img_nand:
            sets_coincide += 1
    legs["b_twist_and_endpoint_locality_controls"] = (
        nand_eq_ok and nand_eq_count == 192 and nand_type_ok
        and pointwise_diff == 1272 and sets_coincide == 69,
        {"nand_passes_type_requirements": (
            "equivariance (192 label-level identities at n = 3, "
            "exhaustive), two-basis class-valuedness on all 69 graphs, "
            "R1 on every dim >= 1 graph, R6 on every dim >= 2 graph -- "
            "the same requirements K3 computes for AND"),
         "pointwise_difference": f"{pointwise_diff} (graph, X) pairs on "
                                 f"the 44 non-bipartite graphs where "
                                 f"char_NAND != char_AND (every X)",
         "weakening_disclosed": f"as SETS the AND and NAND images "
                                f"coincide on all {sets_coincide} of 69 "
                                f"graphs at stated n (computed); the "
                                f"frozen 'different images' is carried "
                                f"as the pointwise class-map statement",
         "imports_named": ["ANTIBALANCED_TWIST_convention (which member "
                           "of the pair obtains is fixed by nothing "
                           "computed here)",
                           "ENDPOINT_LOCALITY_factorization (the rule "
                           "space's defining import; witness executed "
                           "in K3)"]})

    # (c) no represented-side import: set-exact AST probe of own source
    with open(__file__, "r", encoding="utf-8") as fh:
        src = fh.read()
    tree = ast.parse(src)
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "apf" or alias.name.startswith("apf."):
                    found.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and (node.module == "apf"
                                or node.module.startswith("apf.")):
                found.add(node.module)
    legs["c_no_represented_side_import_set_exact"] = (
        found == set(DECLARED_APF_IMPORTS),
        {"declared_apf_imports": sorted(DECLARED_APF_IMPORTS),
         "derived_apf_imports_by_ast": sorted(found),
         "note": "set-exact: this module consumes exactly the join "
                 "network (codomain typing) and the candidate's home "
                 "module (domain typing); no represented-side module "
                 "(elliptope / CHSH / Gram machinery) is imported",
         "bar": "NO identification of the constructed character with "
                "the class the represented side measures is computed, "
                "stated, or implied anywhere in this module -- the S4 "
                "NO-CANONICAL-MAP genre bars assuming it; this control "
                "bars the citation (B4/J4 style, permanent)",
         "limit": "the probe reads import statements only; a "
                  "represented-side value pasted in as a literal would "
                  "evade it (stated limitation, left to audits of the "
                  "source)"})

    # (d) magnitude non-supply, computed; v2-gate facts as records
    pm_ok = True
    pm_count = 0
    for (nn, _P, E) in graphs:
        idx = {e: k for k, e in enumerate(E)}
        basis = _fundamental_cycles(list(range(nn)), E)
        for bits in product((0, 1), repeat=nn):
            memb = {i: bits[i] for i in range(nn)}
            ch = holonomy_character(
                _memb_labels(E, idx, memb, _rule_and), idx, basis)
            pm_ok &= all(isinstance(x, int) and x in (1, -1) for x in ch)
            pm_count += 1
    legs["d_magnitude_non_supply_and_v2_gate_records"] = (
        pm_ok and pm_count == 1888,
        {"outputs_scanned": pm_count,
         "computed": "every character component over every (graph, X) "
                     "pair is a +-1 integer (all 1888 returned outputs "
                     "scanned); SCOPE: an output-level scan -- it reads "
                     "what the map returns, not every internal value",
         "v2_gate_records": [
             "RECORD (not computed here): the frozen v2 gate compares "
             "supplier output against the full datum (class, magnitude) "
             "by exact partition equality in both directions, so a "
             "class-only supplier merges configurations the datum "
             "separates -- structurally unable to pass",
             "RECORD (not computed here): the frozen v2 gate's "
             "configuration type has no alignment/occupancy column, so "
             "an honest occupancy supplier cannot be presented to "
             "eval_supply with its true signature"],
         "routing": "the gate-design question (occupancy column / "
                    "class-only partial supply) is ROUTED TO ETHAN with "
                    "the filed v3 signature-honesty item; it is NOT "
                    "answered in-module"})

    return _result(
        "check_K5_import_controls", legs,
        key_result=(
            f"Permanent import and non-identity controls: (a) the two "
            f"index sets (anchor tokens; ground-set integers) are "
            f"executed and disjoint, the home module's join-count "
            f"identity re-executed over its full {grid}-case grid, and "
            f"NO anchor-to-ground-set map is constructed (iota is a "
            f"named import); (b) AND and NAND both pass every type "
            f"requirement computed here, with class-maps differing "
            f"pointwise on {pointwise_diff} (graph, X) pairs -- the "
            f"twist is a named unforced convention; (c) this module's "
            f"apf imports are set-exactly the join network and the "
            f"candidate's home module -- no represented-side object "
            f"enters, and the identification of the constructed "
            f"character with the measured class is barred, not stated; "
            f"(d) every output component is a +-1 integer over all "
            f"{pm_count} evaluations -- magnitude is not supplied -- "
            f"and the two v2-gate structural facts ride as records with "
            f"the design question routed to Ethan."),
        dependencies=["T_nonlocal_tie_resolution"],
        cross_refs=["continuation_join_network"],
        disclosures=[
            "controls in the B4/J4 style: they compute the two "
            "vocabularies and the convention freedom; they bar the "
            "identifications no successor may quietly claim",
            "the v2-gate items in (d) are RECORDS carried from the "
            "frozen surface, not computations of this module (the "
            "frozen gate file lives outside the repo)"])


# ---------------------------------------------------------------------------
# module surface -- registration (BARE-NAME keys per D6@2026-08-03)
# ---------------------------------------------------------------------------

_CHECKS = {
    "check_K1_coboundary_kill": check_K1_coboundary_kill,
    "check_K2_rule_collapse": check_K2_rule_collapse,
    "check_K3_inhabitation_type_facts": check_K3_inhabitation_type_facts,
    "check_K4_range_obstruction": check_K4_range_obstruction,
    "check_K5_import_controls": check_K5_import_controls,
}


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


def register(registry):
    registry.update({
        "K1_coboundary_kill": check_K1_coboundary_kill,
        "K2_rule_collapse": check_K2_rule_collapse,
        "K3_inhabitation_type_facts": check_K3_inhabitation_type_facts,
        "K4_range_obstruction": check_K4_range_obstruction,
        "K5_import_controls": check_K5_import_controls,
    })
    return registry


if __name__ == "__main__":
    _all = run_all()
    for _name, _r in _all.items():
        print(("PASS" if _r.get("passed") else "FAIL"), _name,
              "legs:", _r.get("leg_count"))
        for _fr in _r.get("fail_reasons", []):
            print("  FAIL-REASON:", _fr)
    print("ALL PASS" if all(r.get("passed") for r in _all.values())
          else "NOT ALL PASS")
