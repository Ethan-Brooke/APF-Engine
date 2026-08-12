"""The continuation join network: Z2 walk composition over sep(P), exactly.

BANKED v24.3.471 (2026-08-12).  Built to the FROZEN claim surface (binding;
J1-J5 adopted verbatim there):
  Artifacts_2026-08-11_session/join_network/CLAIM_SURFACE_FROZEN_2026-08-11.md
  raw sha256: db33433fc4cb0933b21054d12da01ad90d120ebc2c2982eeaacd420c54752e0f
The module may state nothing beyond that surface.  Weakening a claim is the
permitted direction; strengthening is not.

Two blinded cold audits, LAND-WITH-FIXES 0.86 / 0.85, zero arithmetic
disagreement in either; cold fix seat carried (12 fixes, 0 escapes on the
re-run); receipts at Artifacts_2026-08-11_session/join_network/.  LIFTED by
Ethan's ruling 2026-08-12 (record: APF Reference Docs/Reference - DECISION -
Outcome 2 Is Citable and the Join Network Lands (2026-08-12).md).  BARE-NAME
registry keys per D6@2026-08-03.

WHAT THIS MODULE COMPUTES (exact integer arithmetic throughout; Z2 carried as
+-1 integers; no floats on any verdict path; stdlib only)

J1 (check_J1_sep_network_cycle_space).  For every realizable configuration P
at stated n (every set partition of {0..n-1}, n = 3..7): the sep graph (the
cross-block unordered pairs), its component count, and dim H_1 = m - n + c,
computed exactly and cross-checked against the GF(2) incidence rank.  The
>= 3-block census is re-derived in-module (1,028 across n = 3..7 of a
denominator Bell(3..7) = 1,152, with 124 configurations of <= 2 blocks); every
>= 2-block sep graph is verified connected and every >= 3-block one verified
cyclomatic >= 1.  Value tie: `separated_unordered_pairs` (symmetry_cost_floor)
is consumed BY IMPORT and compared field-exact against this module's own sep
edges on the shared orbit-partition domain -- all 1,152 configurations -- not
re-implemented silently.

J2 (check_J2_z2_composition_canonical).  Free Z2 walk composition over sep(P):
identity, involution, and associativity as executed legs; holonomy of closed
walks; then the canonicality battery AS COMPUTED CONTENT --
traversal/rotation/reversal independence, switching invariance with the
coboundary orbit counted exactly (2^(n-1) members per orbit at connected
sep(P)), and character consistency lambda(C1 xor C2) = lambda(C1)*lambda(C2)
over every pattern at stated n.  THE EDGE-LABEL ARGUMENT IS AN EXPLICIT
PARAMETER OF EVERY LEG, NAMED IMPORTED AT THE SITE -- the module computes what
a composition law does WITH labels; it supplies none.

J3 (check_J3_class_character_bijection).  Switching class <-> holonomy
character bijection, exhaustive at stated n: on K3/K4/K5 the switching classes
(union-find over the actual vertex-switching action) number 2/8/64
= 2^(m-n+1); every class's character is computed; injectivity and surjectivity
onto Z2^(m-n+1) are enforced by count.  The same exhaustive method extends to
every complete-multipartite sep graph at n = 4 and n = 5.  THIS IS STATED AS A
FACT ABOUT THE DATUM'S TYPE -- a projection named as a projection -- NEVER AS
A SUPPLY.  Beyond the computed families the general statement is a NAMED
standard-mathematics import (see NAMED_MATH_IMPORTS), consumed if cited, NOT
derived here; no leg's verdict consumes it -- every leg is exhaustive at its
stated n.

J4 (check_J4_enrichment_controls).  (a) The root-fiber control: 384
signed-permutation candidates enumerated; exactly 4 satisfy the tesseract
relation set (transcribed from continuation_tesseract_math and tied to that
module's own executed check); tau-conjugation has 0 fixed points on them --
within the signed-permutation enumeration computed here, any lift of an edge
label to a carrier automorphism has an unforced fiber of at least 4 elements
(exactly 4 in this scope; the general GL4(Q) solution set is larger and not
computed).  (b) The calibration control: exchange covariance holds for an unequal,
non-orthogonal calibration pair (executed through the sibling's own _zipper /
_exchange / _factor_parity), and the banked
T_calibration_free_competition_zipper is executed and its computed freedom
consumed -- cross-join port identification is not supplied by exchange
covariance.  (c) The index-set non-identification control: the parity-cocycle
machinery of graded_orientation_closure (solve_orientation_signs) computes the
same Z2 mathematics on a differently-indexed graph -- verdict-level
coincidence on all 8 triangle sign patterns -- and NO map between its
interface-network index set and any sep(P) is constructed here; carried as a
permanent control in the B4 style, barring the identification no successor may
quietly claim.  (d) Anti-vacuity: a wrong-law mutant (holonomy by sum instead
of product; a basis-dependent reading) fails the named legs, executed in-check
on exhibited patterns.

J5 (check_J5_supply_slot_open).  Two probes and a positive control on the
label slots: every label-consuming function takes `labels` as its explicit
first parameter (signature probe, set-exact against the declared consumer
list); no module-level constant of either scanned shape (an edge-keyed sign
dict; a +-1 sequence) supplies edge labels; and the S2 Case-A collapse runs
as a positive control -- the constant-label network returns the trivial
character on every configuration at stated n.  The probes do not certify the
absence of a supplier in any other shape; three demonstrated evading shapes
are disclosed in the check, and that residual is a stated limitation left to
audits of the source -- no probe here reaches it.

THE ONE LIVE CANDIDATE TYPE (typed here per the frozen surface; BUILT
NOWHERE in this module):  the A12-weakened cycle-space-valued occupancy count
function over QAC input,
    chi_occ : (QAC input at configuration P) -> Hom(H_1(sep(P); Z2), Z2),
a per-configuration character-valued function computed from occupancy counts.
ITS IDENTIFICATION OBLIGATION, NAMED: a demonstration that the class the
represented side measures IS the character this function returns -- the S4
NO-CANONICAL-MAP genre bars assuming it.  Nothing in this module constructs,
approximates, or selects such a function.

LEG INVENTORY (D7@2026-08-08, APPEND-AND-RECORD): _result() compares the
executed leg set against EXPECTED_LEGS set-exactly on the path the bank would
execute; a mismatch contributes a failure reason and does not raise.
STANDING LIMIT, disclosed: this certifies that a declared leg EXECUTED, not
that it COULD HAVE FAILED.

MAY NOT CITE (the frozen surface's list, binding here, carried verbatim):
- Not "the referent is found," not any supply claim, not "the carrier reads
  S" -- J3's bijection is a re-typing of the datum, not a reading of the
  world.
- Not any frustration-class <-> exit-class identification (B4's bar carried
  verbatim; the frustration <-> non-classicality biconditional is
  magnitude-conditional corpus-wide).
- Not any identification among the three Z2 objects (sign class / zipper root
  / orientation cover) -- J4(a) and J4(c) exist to bar exactly that.
- Not evidence for or against situational-S -- the hypothesis stands whatever
  this module computes.
- Not "no banked join network existed" unscoped -- lane-scoped only (the A12
  fence: 8 banked holonomy keys live in a different family).
- Not any statement about record consumption or the Omega door -- the
  character is computed on authored labels; the wall is never met and may not
  be cited as passed.
This module describes what it COMPUTES.  Identity-level legs and choices are
disclosed as such in the returned records.
"""

import inspect
import sys
from itertools import combinations, product

HELD_OUT_OF_THE_BANK = False  # lifted by Ethan's ruling 2026-08-12; banked v24.3.471

CLAIM_SURFACE_SHA256 = (
    "db33433fc4cb0933b21054d12da01ad90d120ebc2c2982eeaacd420c54752e0f")

# Named load-bearing standard-mathematics import (held_connected_subgroup_so2
# disclosure style: recorded machine-readably, consumed if cited beyond the
# computed families, NOT derived here).  No leg's verdict consumes it -- every
# J3 leg is exhaustive at its stated n.
NAMED_MATH_IMPORTS = (
    # switching classes of a signed graph biject with the Z2 cycle-space
    # characters (equivalently, with H^1 of the graph with Z2 coefficients)
    "ZASLAVSKY_1982_SIGNED_GRAPHS_switching_classes_biject_with_Z2_cycle_space_characters",
)

# Transcribed from apf/continuation_tesseract_math.py,
# check_T_quantum_zipper_root_of_exchange (the J4a value tie compares the
# relation-name list against that check's own returned artifact and verifies
# the transcribed Z sits in the enumerated solution set).
TRANSCRIBED_SIGMA = [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]
TRANSCRIBED_TAU = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]]
TRANSCRIBED_J_CONT = [[0, 0, -1, 0], [0, 0, 0, -1],
                      [1, 0, 0, 0], [0, 1, 0, 0]]
TRANSCRIBED_Z = [[1, 0, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0], [0, 1, 0, 0]]
TRANSCRIBED_RELATIONS = ("Z^2=sigma", "Z^4=I", "tau Z tau=Z^-1",
                         "[Z,J_cont]=0")

# The frozen J2 sentence, carried at every label-consuming leg's evidence.
_LABELS_IMPORTED = (
    "the edge-label argument is an explicit parameter of this leg, IMPORTED "
    "at the site (authored by this check for the canonicality battery; "
    "supplied by no banked object)")

EXPECTED_LEGS = {
    "check_J1_sep_network_cycle_space": [
        "census_counts_enforced",
        "dim_h1_matches_gf2_incidence_rank",
        "every_geq2_block_graph_connected",
        "every_geq3_block_graph_cyclomatic_geq_1",
        "sep_pairs_field_exact_tie_by_import",
    ],
    "check_J2_z2_composition_canonical": [
        "associativity_executed_on_walks",
        "character_consistency_every_pattern",
        "edge_involution_self_inverse",
        "holonomy_switching_invariant_on_every_orbit",
        "identity_empty_walk_neutral",
        "switching_orbit_exactly_two_pow_n_minus_one",
        "traversal_rotation_reversal_independence",
        "worked_example_holonomy_of_closed_walks",
    ],
    "check_J3_class_character_bijection": [
        "character_constant_on_each_switching_class",
        "character_injective_across_classes",
        "character_surjective_onto_z2_dim",
        "extension_complete_multipartite_n4_n5",
        "kn_switching_classes_2_8_64_union_find",
    ],
    "check_J4_enrichment_controls": [
        "antivacuity_basis_dependent_reading_fails_named_legs",
        "antivacuity_sum_law_fails_named_legs",
        "calibration_freedom_consumed_and_reexecuted",
        "index_set_non_identification_control",
        "root_fiber_384_to_4_enforced",
        "root_fiber_tau_pairing_zero_fixed_points",
        "root_fiber_transcription_tied_to_upstream",
    ],
    "check_J5_supply_slot_open": [
        "case_a_constant_labels_trivial_character",
        "label_slot_signature_probe",
        "no_module_level_label_supply_probe",
    ],
}


# ---------------------------------------------------------------------------
# exact combinatorial helpers (no labels)
# ---------------------------------------------------------------------------

def _set_partitions(n):
    """All set partitions of {0..n-1}, each a list of lists."""
    if n == 0:
        yield []
        return
    for p in _set_partitions(n - 1):
        for i in range(len(p)):
            yield p[:i] + [p[i] + [n - 1]] + p[i + 1:]
        yield p + [[n - 1]]


def _bell(n):
    """Bell number by the Bell triangle (exact integers)."""
    row = [1]
    for _ in range(n - 1):
        nxt = [row[-1]]
        for x in row:
            nxt.append(nxt[-1] + x)
        row = nxt
    return row[-1] if n > 1 else 1


def _sep_edges(P, n):
    """Cross-block unordered pairs of the partition P -- the sep graph."""
    label = {}
    for k, block in enumerate(P):
        for x in block:
            label[x] = k
    return [(i, j) for i, j in combinations(range(n), 2)
            if label[i] != label[j]]


def _block_generators(P, n):
    """Permutation generators (one cycle per non-singleton block) whose
    orbits on {0..n-1} are exactly the blocks of P -- the shared
    orbit-partition domain for the separated_unordered_pairs tie."""
    gens = []
    for block in P:
        b = sorted(block)
        if len(b) >= 2:
            g = list(range(n))
            for a, nxt in zip(b, b[1:] + b[:1]):
                g[a] = nxt
            gens.append(tuple(g))
    return gens


def _components(verts, edges):
    parent = {v: v for v in verts}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for u, v in edges:
        ra, rb = find(u), find(v)
        if ra != rb:
            parent[ra] = rb
    return len({find(v) for v in verts})


def _gf2_rank(rows):
    """Rank over GF(2) of bitmask rows."""
    piv = {}
    for r in rows:
        cur = r
        while cur:
            h = cur.bit_length() - 1
            if h in piv:
                cur ^= piv[h]
            else:
                piv[h] = cur
                break
    return len(piv)


def _fundamental_cycles(verts, edges):
    """Fundamental cycles w.r.t. a BFS spanning forest (roots at the
    smallest vertex of each component).  Each cycle is a sorted tuple of
    edges; the list is ordered by the non-tree edge, in edge-list order."""
    adj = {v: [] for v in verts}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    parent = {}
    depth = {}
    tree = set()
    for root in verts:
        if root in depth:
            continue
        depth[root] = 0
        parent[root] = None
        queue = [root]
        for u in queue:
            for v in sorted(adj[u]):
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


# ---------------------------------------------------------------------------
# label-consuming functions.  `labels` is the EXPLICIT first parameter of
# every one (the J5 signature probe enforces this set-exactly): labels is a
# tuple of +-1 in edge-index order, IMPORTED by the caller; this module
# supplies none.
# ---------------------------------------------------------------------------

def walk_value(labels, edge_index, walk_edges):
    """Z2 value of a walk given as a sequence of edges: the product of the
    imported labels along it.  The empty walk is the identity (+1)."""
    h = 1
    for e in walk_edges:
        h *= labels[edge_index[e]]
    return h


def holonomy_of_cycle(labels, edge_index, cycle_edges):
    """Z2 holonomy of a closed walk / cycle-space element given as an edge
    collection: the product of the imported labels over it."""
    h = 1
    for e in cycle_edges:
        h *= labels[edge_index[e]]
    return h


def closed_walk_value(labels, edge_index, vertex_cycle):
    """Z2 value of a closed walk given as an ordered vertex cycle -- the
    traversal-order evaluator the invariance legs compare against."""
    h = 1
    for a, b in zip(vertex_cycle, tuple(vertex_cycle[1:]) + (vertex_cycle[0],)):
        e = (a, b) if a < b else (b, a)
        h *= labels[edge_index[e]]
    return h


def holonomy_character(labels, edge_index, fundamental_cycles):
    """The holonomy character: the tuple of Z2 holonomies over the given
    fundamental cycles."""
    return tuple(holonomy_of_cycle(labels, edge_index, c)
                 for c in fundamental_cycles)


def switch_pattern(labels, edge_index, edges, vertex):
    """Vertex switching: flip the imported label on every edge incident to
    `vertex`; return the switched pattern."""
    out = list(labels)
    for e in edges:
        if vertex in e:
            out[edge_index[e]] = -out[edge_index[e]]
    return tuple(out)


def coboundary_orbit(labels, edge_index, edges, verts):
    """The full switching (coboundary) orbit of the imported pattern: apply
    every subset of vertex switchings."""
    vl = list(verts)
    out = set()
    for mask in product((0, 1), repeat=len(vl)):
        q = tuple(labels)
        for v, bit in zip(vl, mask):
            if bit:
                q = switch_pattern(q, edge_index, edges, v)
        out.add(q)
    return out


# ---------------------------------------------------------------------------
# switching classes by union-find over the ACTUAL switching action
# ---------------------------------------------------------------------------

def _switching_classes(edges, verts):
    m = len(edges)
    idx = {e: k for k, e in enumerate(edges)}
    pats = list(product((1, -1), repeat=m))
    pos = {p: i for i, p in enumerate(pats)}
    parent = list(range(len(pats)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i, p in enumerate(pats):
        for v in verts:
            q = switch_pattern(p, idx, edges, v)
            ra, rb = find(i), find(pos[q])
            if ra != rb:
                parent[ra] = rb
    classes = {}
    for i, p in enumerate(pats):
        classes.setdefault(find(i), []).append(p)
    return pats, idx, list(classes.values())


# ---------------------------------------------------------------------------
# 4x4 integer matrix helpers (root-fiber control)
# ---------------------------------------------------------------------------

def _mm4(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)]
            for i in range(4)]


_I4 = [[1 if i == j else 0 for j in range(4)] for i in range(4)]


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
        "named_math_imports": list(NAMED_MATH_IMPORTS),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "frozen_claim_surface_sha256": CLAIM_SURFACE_SHA256,
        "inventory_note": (
            "append-and-record (D7@2026-08-08): certifies a declared leg "
            "EXECUTED, not that it could have failed"),
    }


# ---------------------------------------------------------------------------
# J1 -- the network object
# ---------------------------------------------------------------------------

def check_J1_sep_network_cycle_space():
    """J1: sep(P), components, dim H_1 = m - n + c for every configuration
    at n = 3..7; the 1,028 census re-derived; connectivity and cyclomatic
    floors verified; separated_unordered_pairs consumed by import and
    compared field-exact on the shared orbit-partition domain."""
    from apf.symmetry_cost_floor import separated_unordered_pairs

    legs = {}
    total = geq3 = leq2 = 0
    bell_sum = sum(_bell(n) for n in range(3, 8))
    tie_ok = True
    tie_count = 0
    conn_ok = True
    conn_count = 0
    cyc_ok = True
    h1_ok = True
    h1_count = 0
    for n in range(3, 8):
        for P in _set_partitions(n):
            total += 1
            E = _sep_edges(P, n)
            m = len(E)
            c = _components(list(range(n)), E)
            h1 = m - n + c
            rank = _gf2_rank([(1 << i) | (1 << j) for i, j in E])
            h1_ok &= (rank == n - c) and (h1 == m - rank)
            h1_count += 1
            gens = _block_generators(P, n)
            sp = sorted(tuple(e) for e in separated_unordered_pairs(gens, n))
            tie_ok &= (sp == sorted(E))
            tie_count += 1
            if len(P) >= 3:
                geq3 += 1
                cyc_ok &= (h1 >= 1)
            else:
                leq2 += 1
            if len(P) >= 2:
                conn_count += 1
                conn_ok &= (c == 1)

    legs["census_counts_enforced"] = (
        total == 1152 and total == bell_sum and geq3 == 1028
        and leq2 == 124 and geq3 + leq2 == total,
        {"total_configurations_n_3_to_7": total,
         "bell_3_to_7_sum": bell_sum,
         "geq3_block": geq3, "leq2_block": leq2,
         "note": "denominator re-derived live by Bell-triangle recurrence "
                 "and by enumeration; the 1,028 / 1,152 / 124 pins are the "
                 "S1 Certificate A / L7 value tie"})
    legs["sep_pairs_field_exact_tie_by_import"] = (
        tie_ok and tie_count == total,
        {"configurations_compared": tie_count,
         "source": "symmetry_cost_floor.separated_unordered_pairs, "
                   "consumed by import",
         "domain": "for each partition, generators whose orbits are its "
                   "blocks; comparison is exact tuple-list equality of the "
                   "sep-pair sets"})
    legs["every_geq2_block_graph_connected"] = (
        conn_ok and conn_count == total - 5,
        {"geq2_block_graphs_checked": conn_count,
         "note": "the 5 excluded configurations are the one-block partition "
                 "at each n in 3..7 (empty sep graph, c = n)"})
    legs["every_geq3_block_graph_cyclomatic_geq_1"] = (
        cyc_ok and geq3 == 1028,
        {"geq3_block_graphs_checked": geq3})
    legs["dim_h1_matches_gf2_incidence_rank"] = (
        h1_ok and h1_count == total,
        {"configurations_cross_checked": h1_count,
         "note": "dim H_1 = m - n + c computed by the component formula and "
                 "independently as m - rank_GF2(incidence)"})

    return _result(
        "check_J1_sep_network_cycle_space", legs,
        key_result=(
            f"Across n = 3..7: {total} configurations (= Bell(3..7) = "
            f"{bell_sum}), of which {geq3} have >= 3 blocks and {leq2} have "
            f"<= 2; every >= 2-block sep graph is connected "
            f"({conn_count} checked) and every >= 3-block one has "
            f"dim H_1 = m - n + c >= 1; the sep pairs agree field-exactly "
            f"with separated_unordered_pairs on all {tie_count} "
            f"configurations."),
        cross_refs=["symmetry_cost_floor.separated_unordered_pairs"],
        disclosures=[
            "the sep graph of a partition is complete multipartite by "
            "construction; that identity is used, not measured",
            "value tie: the 1,028 census is the S1 Certificate A / L7 "
            "figure, re-derived here rather than quoted"])


# ---------------------------------------------------------------------------
# J2 -- the composition law and its canonicality legs
# ---------------------------------------------------------------------------

def check_J2_z2_composition_canonical():
    """J2: free Z2 walk composition over sep(P) at stated n (all >= 2-block
    configurations at n = 4, plus K3 for the traversal leg); identity,
    involution, associativity executed; holonomy of closed walks; the
    canonicality battery as computed content.  Labels are IMPORTED
    parameters at every leg; this module supplies none."""
    legs = {}
    n = 4
    graphs = [(_sep_edges(P, n), len(P)) for P in _set_partitions(n)
              if len(P) >= 2]
    n_graphs = len(graphs)
    bell_n_minus_1 = _bell(n) - 1

    # K4 = the discrete partition's sep graph
    k4_edges = [e for e, blocks in graphs if blocks == n][0]
    k4_idx = {e: k for k, e in enumerate(k4_edges)}
    k4_pats = list(product((1, -1), repeat=len(k4_edges)))
    k4_basis = _fundamental_cycles(list(range(n)), k4_edges)

    # identity: the empty walk is neutral, on every K4 pattern
    w_sample = ((0, 1), (1, 2))
    id_ok = all(
        walk_value(p, k4_idx, ()) == 1
        and walk_value(p, k4_idx, w_sample + ()) == walk_value(
            p, k4_idx, w_sample)
        for p in k4_pats)
    legs["identity_empty_walk_neutral"] = (
        id_ok and len(k4_pats) == 2 ** len(k4_edges),
        {"patterns": len(k4_pats),
         "leg_class": "identity-level control, not a measurement (the "
                      "frozen surface's named axiom, executed on the "
                      "actual implementation)",
         "labels": _LABELS_IMPORTED})

    # involution: every edge is its own inverse, over every >= 2-block
    # sep graph at n = 4 and every pattern
    inv_ok = True
    inv_graphs = 0
    for E, _blocks in graphs:
        idx = {e: k for k, e in enumerate(E)}
        inv_graphs += 1
        for p in product((1, -1), repeat=len(E)):
            for e in E:
                inv_ok &= (p[idx[e]] * p[idx[e]] == 1
                           and walk_value(p, idx, (e, e)) == 1)
    legs["edge_involution_self_inverse"] = (
        inv_ok and inv_graphs == n_graphs and n_graphs == bell_n_minus_1,
        {"graphs": inv_graphs,
         "note": f"all >= 2-block configurations at n = {n} "
                 f"(= Bell({n}) - 1 = {bell_n_minus_1})",
         "leg_class": "identity-level control, not a measurement (the "
                      "frozen surface's named axiom, executed on the "
                      "actual implementation)",
         "labels": _LABELS_IMPORTED})

    # associativity: concatenation of walks is associative structurally and
    # the value map is a homomorphism, on every K4 pattern
    w1, w2, w3 = ((0, 1), (1, 2)), ((2, 3),), ((0, 3), (0, 2))
    assoc_ok = ((w1 + w2) + w3 == w1 + (w2 + w3))
    for p in k4_pats:
        assoc_ok &= (walk_value(p, k4_idx, (w1 + w2) + w3)
                     == walk_value(p, k4_idx, w1 + (w2 + w3)))
        assoc_ok &= (walk_value(p, k4_idx, w1 + w2)
                     == walk_value(p, k4_idx, w1) * walk_value(p, k4_idx, w2))
    legs["associativity_executed_on_walks"] = (
        assoc_ok,
        {"patterns": len(k4_pats),
         "leg_class": "identity-level control, not a measurement "
                      "(integer multiplication is associative; the leg "
                      "executes the frozen surface's named axiom on the "
                      "actual composition implementation)",
         "labels": _LABELS_IMPORTED})

    # traversal / rotation / reversal independence: every triangle of K3
    # and K4, every pattern, all 6 traversals agree with the edge-set
    # holonomy
    trav_ok = True
    trav_comparisons = 0
    for nn in (3, 4):
        E = [(i, j) for i, j in combinations(range(nn), 2)]
        idx = {e: k for k, e in enumerate(E)}
        tris = list(combinations(range(nn), 3))
        for p in product((1, -1), repeat=len(E)):
            for tri in tris:
                base = holonomy_of_cycle(
                    p, idx, [(tri[0], tri[1]), (tri[1], tri[2]),
                             (tri[0], tri[2])])
                for rot in range(3):
                    seq = tri[rot:] + tri[:rot]
                    for order in (seq, tuple(reversed(seq))):
                        trav_ok &= (closed_walk_value(p, idx, order) == base)
                        trav_comparisons += 1
    expected_trav = (2 ** 3) * 1 * 6 + (2 ** 6) * 4 * 6
    legs["traversal_rotation_reversal_independence"] = (
        trav_ok and trav_comparisons == expected_trav,
        {"comparisons": trav_comparisons,
         "expected": expected_trav,
         "note": "K3 and K4, every pattern, every triangle, 3 rotations x "
                 "2 directions, each against the unordered edge-set "
                 "holonomy",
         "labels": _LABELS_IMPORTED})

    # switching orbit exactly 2^(n-1), and holonomy character constant on
    # every orbit -- every >= 2-block sep graph at n = 4, every pattern
    orbit_ok = True
    invar_ok = True
    orbit_checked = 0
    for E, _blocks in graphs:
        idx = {e: k for k, e in enumerate(E)}
        basis = _fundamental_cycles(list(range(n)), E)
        for p in product((1, -1), repeat=len(E)):
            orb = coboundary_orbit(p, idx, E, range(n))
            orbit_ok &= (len(orb) == 2 ** (n - 1))
            orbit_checked += 1
            ch = holonomy_character(p, idx, basis)
            invar_ok &= all(
                holonomy_character(q, idx, basis) == ch for q in orb)
    legs["switching_orbit_exactly_two_pow_n_minus_one"] = (
        orbit_ok and orbit_checked == sum(2 ** len(E) for E, _b in graphs),
        {"pattern_verifications": orbit_checked,
         "orbit_size_each": 2 ** (n - 1),
         "note": f"connected sep(P) at n = {n}: the coboundary kernel is "
                 f"the global flip, so every orbit has 2^({n}-1) members",
         "labels": _LABELS_IMPORTED})
    legs["holonomy_switching_invariant_on_every_orbit"] = (
        invar_ok,
        {"pattern_verifications": orbit_checked,
         "labels": _LABELS_IMPORTED})

    # character consistency lambda(C1 xor C2) = lambda(C1)*lambda(C2), every
    # pattern, every pair of fundamental cycles, every graph with >= 2
    # fundamental cycles; plus the explicit K4 dependent triangle
    cons_ok = True
    cons_pairs = 0
    graphs_with_pairs = 0
    for E, _blocks in graphs:
        idx = {e: k for k, e in enumerate(E)}
        basis = _fundamental_cycles(list(range(n)), E)
        if len(basis) < 2:
            continue
        graphs_with_pairs += 1
        for c1, c2 in combinations(basis, 2):
            xor = tuple(sorted(set(c1) ^ set(c2)))
            cons_pairs += 1
            for p in product((1, -1), repeat=len(E)):
                cons_ok &= (
                    holonomy_of_cycle(p, idx, xor)
                    == holonomy_of_cycle(p, idx, c1)
                    * holonomy_of_cycle(p, idx, c2))
    t123 = ((1, 2), (1, 3), (2, 3))
    xor_all = set()
    for c in k4_basis:
        xor_all ^= set(c)
    dep_ok = (xor_all == set(t123))
    for p in k4_pats:
        rhs = 1
        for c in k4_basis:
            rhs *= holonomy_of_cycle(p, k4_idx, c)
        dep_ok &= (holonomy_of_cycle(p, k4_idx, t123) == rhs)
    legs["character_consistency_every_pattern"] = (
        cons_ok and dep_ok and graphs_with_pairs == 7,
        {"graphs_with_cycle_pairs": graphs_with_pairs,
         "fundamental_cycle_pairs": cons_pairs,
         "k4_dependent_triangle": "(1,2,3) = xor of the three basis "
                                  "triangles, verified structurally and on "
                                  "every pattern",
         "labels": _LABELS_IMPORTED})

    # holonomy of closed walks: the worked n = 4 example (S = all +1 except
    # edge (0,1)), character and coboundary orbit pinned
    S = tuple(-1 if e == (0, 1) else 1 for e in k4_edges)
    ch = holonomy_character(S, k4_idx, k4_basis)
    orb = coboundary_orbit(S, k4_idx, k4_edges, range(n))
    same = all(holonomy_character(q, k4_idx, k4_basis) == ch for q in orb)
    legs["worked_example_holonomy_of_closed_walks"] = (
        ch == (-1, -1, 1) and len(orb) == 2 ** (n - 1) and same,
        {"pattern": "all +1 except edge (0,1)",
         "basis_triangles": tuple(
             tuple(sorted({v for edge in cyc for v in edge}))
             for cyc in k4_basis),
         "character": ch, "orbit_members": len(orb),
         "labels": _LABELS_IMPORTED})

    return _result(
        "check_J2_z2_composition_canonical", legs,
        key_result=(
            f"Free Z2 walk composition over sep(P) at n = {n}: identity, "
            f"involution and associativity executed; traversal invariance "
            f"({trav_comparisons} comparisons at K3/K4); switching orbits "
            f"of exactly {2 ** (n - 1)} members verified once per pattern "
            f"({orbit_checked} pattern-level verifications across "
            f"{n_graphs} connected sep graphs), with "
            f"the holonomy character constant on every orbit; character "
            f"consistency on every pattern over {cons_pairs} fundamental "
            f"pairs; worked example character {ch}.  The labels are "
            f"imported parameters at every leg; this module supplies none."),
        cross_refs=[],
        disclosures=[
            "the module computes what a composition law does WITH labels; "
            "it supplies none (the frozen J2 sentence, carried at every "
            "leg's evidence)",
            "stated scope: pattern-exhaustive legs run at n = 4 (all "
            ">= 2-block configurations) and K3; nothing is claimed beyond "
            "the stated n"])


# ---------------------------------------------------------------------------
# J3 -- the re-typing theorem
# ---------------------------------------------------------------------------

def check_J3_class_character_bijection():
    """J3: switching class <-> holonomy character bijection, exhaustive at
    stated n.  A fact about the DATUM'S TYPE -- a projection named as a
    projection -- never a supply."""
    legs = {}
    pinned = {3: 2, 4: 8, 5: 64}
    count_ok = True
    const_ok = True
    inj_ok = True
    surj_ok = True
    kn_rows = {}
    for n in (3, 4, 5):
        E = [(i, j) for i, j in combinations(range(n), 2)]
        m = len(E)
        _pats, idx, classes = _switching_classes(E, range(n))
        dim = m - n + 1
        count_ok &= (len(classes) == pinned[n]
                     and len(classes) == 2 ** dim)
        basis = _fundamental_cycles(list(range(n)), E)
        chars = []
        for cls in classes:
            cs = {holonomy_character(p, idx, basis) for p in cls}
            const_ok &= (len(cs) == 1)
            chars.append(next(iter(cs)))
        inj_ok &= (len(set(chars)) == len(chars))
        surj_ok &= (len(set(chars)) == 2 ** dim)
        kn_rows[n] = {"classes": len(classes), "dim": dim,
                      "distinct_characters": len(set(chars))}

    legs["kn_switching_classes_2_8_64_union_find"] = (
        count_ok and len(kn_rows) == 3,
        {"rows": {str(k): v for k, v in kn_rows.items()},
         "note": "union-find over the actual vertex-switching action; "
                 "counts enforced against the pinned 2/8/64 AND the live "
                 "2^(m-n+1)",
         "labels": _LABELS_IMPORTED})
    legs["character_constant_on_each_switching_class"] = (
        const_ok, {"scope": "K3/K4/K5, every class, every member",
                   "labels": _LABELS_IMPORTED})
    legs["character_injective_across_classes"] = (
        inj_ok, {"scope": "K3/K4/K5, all classes pairwise"})
    legs["character_surjective_onto_z2_dim"] = (
        surj_ok,
        {"scope": "K3/K4/K5: distinct characters number exactly "
                  "2^(m-n+1)"})

    # extension: every complete-multipartite sep graph at n = 4 and n = 5
    ext_ok = True
    ext_rows = {}
    for n in (4, 5):
        graphs = [_sep_edges(P, n) for P in _set_partitions(n)
                  if len(P) >= 2]
        ext_rows[n] = len(graphs)
        ext_ok &= (len(graphs) == _bell(n) - 1)
        for E in graphs:
            m = len(E)
            _pats, idx, classes = _switching_classes(E, range(n))
            dim = m - n + 1
            ext_ok &= (len(classes) == 2 ** dim)
            basis = _fundamental_cycles(list(range(n)), E)
            chars = []
            for cls in classes:
                cs = {holonomy_character(p, idx, basis) for p in cls}
                ext_ok &= (len(cs) == 1)
                chars.append(next(iter(cs)))
            ext_ok &= (len(set(chars)) == len(chars) == 2 ** dim)
    legs["extension_complete_multipartite_n4_n5"] = (
        ext_ok and ext_rows == {4: 14, 5: 51},
        {"graphs": {str(k): v for k, v in ext_rows.items()},
         "note": "every >= 2-block configuration's sep graph (all complete "
                 "multipartite, all connected), same exhaustive method: "
                 "class count 2^(m-n+1) and class <-> character bijection "
                 "enforced per graph",
         "labels": _LABELS_IMPORTED})

    return _result(
        "check_J3_class_character_bijection", legs,
        key_result=(
            f"Switching class <-> holonomy character is a BIJECTION, "
            f"exhaustively: K3/K4/K5 give {kn_rows[3]['classes']}/"
            f"{kn_rows[4]['classes']}/{kn_rows[5]['classes']} classes "
            f"= 2^(m-n+1), each with one character, all distinct, "
            f"surjective onto Z2^(m-n+1); the same holds for every "
            f"complete-multipartite sep graph at n = 4 ({ext_rows[4]} "
            f"graphs) and n = 5 ({ext_rows[5]} graphs).  This is a fact "
            f"about the datum's TYPE -- a projection named as a projection "
            f"-- not a supply."),
        cross_refs=[],
        disclosures=[
            "value tie: 2/8/64 is A12's executed arm and the frozen T1.2 "
            "provenance, re-derived here by union-find over the actual "
            "action",
            "beyond the computed families the general statement is the "
            "NAMED standard-mathematics import in NAMED_MATH_IMPORTS "
            "(Zaslavsky), consumed if cited, not derived here; no leg's "
            "verdict consumes it",
            "scope bound: exhaustive at the stated n only (K3/K4/K5 and "
            "all sep graphs at n = 4, 5); c > 1 sep graphs do not occur at "
            ">= 2 blocks and are not covered"])


# ---------------------------------------------------------------------------
# J4 -- non-identity and enrichment-obstruction controls
# ---------------------------------------------------------------------------

def check_J4_enrichment_controls():
    """J4: the root-fiber control (384 -> 4, 0 tau-fixed), the calibration
    control (consumed and re-executed), the index-set non-identification
    control, and the executed anti-vacuity mutants."""
    import apf.continuation_tesseract_math as ctm
    from apf.graded_orientation_closure import solve_orientation_signs
    from fractions import Fraction as Fr

    legs = {}

    # (a) root fiber: enumerate all 384 signed permutations
    perms = [p for p in product(range(4), repeat=4) if len(set(p)) == 4]
    count_enum = 0
    sols = []
    for p in perms:
        for signs in product((1, -1), repeat=4):
            count_enum += 1
            R = [[0] * 4 for _ in range(4)]
            for i in range(4):
                R[i][p[i]] = signs[i]
            R2 = _mm4(R, R)
            if R2 != TRANSCRIBED_SIGMA:
                continue
            if _mm4(R2, R2) != _I4:
                continue
            if _mm4(_mm4(_mm4(TRANSCRIBED_TAU, R), TRANSCRIBED_TAU),
                    R) != _I4:
                continue
            if _mm4(R, TRANSCRIBED_J_CONT) != _mm4(TRANSCRIBED_J_CONT, R):
                continue
            sols.append(R)
    legs["root_fiber_384_to_4_enforced"] = (
        count_enum == 384 and len(perms) == 24 and len(sols) == 4,
        {"candidates_enumerated": count_enum, "solutions": len(sols),
         "note": "signed-permutation-scoped, matching the S2 P2 "
                 "disclosure; the general GL4(Q) solution set is larger "
                 "and not computed here"})

    conj = [_mm4(_mm4(TRANSCRIBED_TAU, R), TRANSCRIBED_TAU) for R in sols]
    fixed = sum(1 for R, C in zip(sols, conj) if R == C)
    orbit_pairs = []
    pairing_total = True
    used = set()
    for i, R in enumerate(sols):
        if i in used:
            continue
        j = next((k for k, S in enumerate(sols) if S == conj[i]), None)
        if j is None:
            # tau-conjugate left the solution set: record, do not raise
            pairing_total = False
            used.add(i)
            continue
        used |= {i, j}
        orbit_pairs.append((i, j))
    legs["root_fiber_tau_pairing_zero_fixed_points"] = (
        fixed == 0 and pairing_total and len(orbit_pairs) == 2
        and all(i != j for i, j in orbit_pairs),
        {"tau_fixed_points": fixed, "tau_orbits_of_size_2": len(orbit_pairs),
         "note": "within the signed-permutation enumeration computed here, "
                 "any lift of an edge label to a carrier automorphism has an "
                 "unforced fiber of at least 4 elements (exactly 4 in this "
                 "scope; the sibling leg discloses the general GL4(Q) "
                 "solution set is larger, not computed); nothing here "
                 "selects"})

    r_up = ctm.check_T_quantum_zipper_root_of_exchange()
    legs["root_fiber_transcription_tied_to_upstream"] = (
        r_up.get("passed") is True
        and list(r_up["artifacts"]["relations"])
        == list(TRANSCRIBED_RELATIONS)
        and TRANSCRIBED_Z in sols
        and _mm4(TRANSCRIBED_Z, TRANSCRIBED_Z) == TRANSCRIBED_SIGMA,
        {"upstream_check": "T_quantum_zipper_root_of_exchange (executed)",
         "relations_artifact_matches_transcription": True,
         "transcribed_Z_is_a_solution": TRANSCRIBED_Z in sols,
         "tie_scope": "the tie consumes exactly two upstream values -- "
                      "the passed verdict and the relation-name list -- "
                      "and verifies the transcribed Z solves the "
                      "transcribed relations; ANY upstream change that "
                      "preserves those two values (drift in sigma, tau, "
                      "J_cont or Z, or wholesale replacement of the "
                      "upstream computation) is not detected by this leg "
                      "(disclosed)"})

    # (b) calibration control: consumed AND re-executed through the
    # sibling's own functions
    r_cal = ctm.check_T_calibration_free_competition_zipper()
    a_cal = [[Fr(1), Fr(1)], [Fr(0), Fr(1)]]
    d_cal = [[Fr(5), Fr(2)], [Fr(1), Fr(1)]]
    xi = ctm._zipper(a_cal, d_cal)
    cov = ctm._eq(ctm._mm(xi, ctm._exchange(2)),
                  ctm._mm(ctm._factor_parity(2), xi))
    inv_ok = ctm._eq(ctm._mm(ctm._zipper_inverse(a_cal, d_cal), xi),
                     ctm._eye(4))
    i4f = ctm._eye(4)
    bad_fails = not ctm._eq(ctm._mm(i4f, ctm._exchange(2)),
                            ctm._mm(ctm._factor_parity(2), i4f))
    legs["calibration_freedom_consumed_and_reexecuted"] = (
        r_cal.get("passed") is True
        and r_cal["artifacts"]["equal_calibration_required"] is False
        and r_cal["artifacts"]["metric_used"] is False
        and a_cal != d_cal and cov and inv_ok and bad_fails,
        {"banked_check": "T_calibration_free_competition_zipper (executed; "
                         "equal_calibration_required is False in its own "
                         "returned artifacts)",
         "own_reexecution": "an unequal, non-orthogonal pair (a, d) passes "
                            "exchange covariance through the sibling's own "
                            "_zipper/_exchange/_factor_parity and is "
                            "invertible; the identity control fails "
                            "covariance",
         "reading": "exchange covariance does not supply cross-join port "
                    "identification (equal calibration, orthogonality, a "
                    "norm, reciprocity are all unforced -- the sibling's "
                    "computed freedom, consumed not re-proved)"})

    # (c) index-set non-identification control
    tri_edges = [(0, 1), (0, 2), (1, 2)]
    tri_idx = {e: k for k, e in enumerate(tri_edges)}
    agree = 0
    total8 = 0
    ok_c = True
    for e01, e02, e12 in product((1, -1), repeat=3):
        total8 += 1
        theirs = solve_orientation_signs(
            ("A", "B", "C"),
            (("A", "B", e01), ("B", "C", e12), ("C", "A", e02)))
        pattern = (e01, e02, e12)
        mine = holonomy_of_cycle(pattern, tri_idx, tri_edges)
        same = (theirs["orientable"] == (mine == 1))
        ok_c &= same
        agree += same
    legs["index_set_non_identification_control"] = (
        ok_c and total8 == 8 and agree == 8,
        {"triangle_sign_patterns": total8, "verdict_agreements": agree,
         "note": "graded_orientation_closure.solve_orientation_signs "
                 "computes the same Z2 mathematics on ITS OWN "
                 "string-indexed interface network; the comparison here "
                 "pairs each abstract sign tuple with itself and "
                 "constructs NO map between that index set and any "
                 "sep(P); the coincidence is function-level (permanent "
                 "control, B4 style)",
         "labels": _LABELS_IMPORTED})

    # (d) anti-vacuity: the wrong laws FAIL the named legs, on exhibits
    k4_edges = [(i, j) for i, j in combinations(range(4), 2)]
    k4_idx = {e: k for k, e in enumerate(k4_edges)}
    k4_basis = _fundamental_cycles(list(range(4)), k4_edges)

    def _sum_law(labels, edge_index, cycle_edges):
        h = 0
        for e in cycle_edges:
            h += labels[edge_index[e]]
        return h

    all_plus = (1,) * 6
    c1, c2 = k4_basis[0], k4_basis[1]
    xor12 = tuple(sorted(set(c1) ^ set(c2)))
    sum_consistency_fails = (
        _sum_law(all_plus, k4_idx, xor12)
        != _sum_law(all_plus, k4_idx, c1) + _sum_law(all_plus, k4_idx, c2))
    right_consistency_holds = (
        holonomy_of_cycle(all_plus, k4_idx, xor12)
        == holonomy_of_cycle(all_plus, k4_idx, c1)
        * holonomy_of_cycle(all_plus, k4_idx, c2))
    switched = switch_pattern(all_plus, k4_idx, k4_edges, 0)
    sum_invariance_fails = (
        _sum_law(switched, k4_idx, c1) != _sum_law(all_plus, k4_idx, c1))
    right_invariance_holds = (
        holonomy_of_cycle(switched, k4_idx, c1)
        == holonomy_of_cycle(all_plus, k4_idx, c1))
    legs["antivacuity_sum_law_fails_named_legs"] = (
        sum_consistency_fails and sum_invariance_fails
        and right_consistency_holds and right_invariance_holds,
        {"exhibit": "K4, all-plus pattern; switching at vertex 0",
         "sum_law_breaks": "character consistency AND switching invariance",
         "product_law_holds_on_the_same_exhibits": True,
         "labels": _LABELS_IMPORTED})

    def _first_edge_reading(labels, edge_index, vertex_cycle):
        a, b = vertex_cycle[0], vertex_cycle[1]
        e = (a, b) if a < b else (b, a)
        return labels[edge_index[e]]

    S = tuple(-1 if e == (0, 1) else 1 for e in k4_edges)
    tri = (0, 1, 2)
    readings = {_first_edge_reading(S, k4_idx, tri[r:] + tri[:r])
                for r in range(3)}
    basis_dep_traversal_fails = (len(readings) > 1)
    S_sw = switch_pattern(S, k4_idx, k4_edges, 2)
    basis_dep_switching_fails = (
        _first_edge_reading(S_sw, k4_idx, (2, 0, 1))
        != _first_edge_reading(S, k4_idx, (2, 0, 1)))
    right_traversal_holds = (
        len({closed_walk_value(S, k4_idx, tri[r:] + tri[:r])
             for r in range(3)}) == 1)
    legs["antivacuity_basis_dependent_reading_fails_named_legs"] = (
        basis_dep_traversal_fails and basis_dep_switching_fails
        and right_traversal_holds,
        {"exhibit": "K4, one negative edge (0,1); triangle (0,1,2)",
         "wrong_reading": "the label of the first traversed edge",
         "breaks": "traversal independence AND switching invariance",
         "product_law_holds_on_the_same_exhibit": True,
         "labels": _LABELS_IMPORTED})

    return _result(
        "check_J4_enrichment_controls", legs,
        key_result=(
            f"Enrichment controls: {count_enum} signed-permutation "
            f"candidates yield exactly {len(sols)} solutions of the "
            f"transcribed tesseract relations with {fixed} tau-fixed "
            f"points (an unforced fiber for any carrier lift -- 4 elements "
            f"in the signed-permutation scope computed here); "
            f"exchange covariance holds for an unequal calibration pair "
            f"(the banked freedom, consumed and re-executed); the "
            f"parity-cocycle sibling agrees verdict-for-verdict on all "
            f"{total8} triangle sign patterns with no index map "
            f"constructed; both wrong-law mutants fail the named legs on "
            f"exhibited patterns."),
        dependencies=["T_quantum_zipper_root_of_exchange",
                      "T_calibration_free_competition_zipper"],
        cross_refs=["graded_orientation_closure.solve_orientation_signs"],
        disclosures=[
            "value ties: the 384 -> 4 / 0-fixed fiber is S2 probe P2, "
            "re-derived; the calibration freedom is "
            "T_calibration_free_competition_zipper's, consumed "
            "(cross_refs -> dependencies, since executed)",
            "no identification among the three Z2 objects (sign class / "
            "zipper root / orientation cover) is computed here; legs (a) "
            "and (c) compute the controls the frozen surface names"])


# ---------------------------------------------------------------------------
# J5 -- the supply-side containment
# ---------------------------------------------------------------------------

LABEL_PARAM_FUNCTIONS = (
    "closed_walk_value",
    "coboundary_orbit",
    "holonomy_character",
    "holonomy_of_cycle",
    "switch_pattern",
    "walk_value",
)


def check_J5_supply_slot_open():
    """J5: two probes on the label slots (signature set-exactness; a scan
    for module-level constants of two label-supplying shapes) and the S2
    Case-A collapse as positive control."""
    legs = {}
    mod = sys.modules[__name__]

    # signature probe: the label-consuming functions, set-exactly
    found = sorted(
        nm for nm, fn in vars(mod).items()
        if inspect.isfunction(fn)
        and fn.__module__ == __name__
        and not nm.startswith("check_")
        and "labels" in inspect.signature(fn).parameters)
    first_param_ok = all(
        next(iter(inspect.signature(getattr(mod, nm)).parameters))
        == "labels"
        for nm in LABEL_PARAM_FUNCTIONS)
    legs["label_slot_signature_probe"] = (
        found == sorted(LABEL_PARAM_FUNCTIONS) and first_param_ok,
        {"declared_consumers": sorted(LABEL_PARAM_FUNCTIONS),
         "derived_consumers": found,
         "note": "set-exact: the functions taking a `labels` parameter are "
                 "exactly the declared consumers, and `labels` is the "
                 "first parameter of each -- the label slot is an explicit "
                 "argument everywhere, supplied by the caller"})

    # no module-level label supply
    dict_suppliers = [
        nm for nm, v in vars(mod).items()
        if isinstance(v, dict) and v
        and all(isinstance(k, tuple) and len(k) == 2
                and all(isinstance(x, int) for x in k) for k in v)
        and all(x in (1, -1) for x in v.values())]
    seq_suppliers = [
        nm for nm, v in vars(mod).items()
        if isinstance(v, (tuple, list)) and len(v) >= 3
        and all(isinstance(x, int) and x in (1, -1) for x in v)]
    legs["no_module_level_label_supply_probe"] = (
        dict_suppliers == [] and seq_suppliers == [],
        {"edge_keyed_sign_dicts_at_module_level": dict_suppliers,
         "sign_sequences_at_module_level": seq_suppliers,
         "note": "a module-level object of either scanned shape (an "
                 "edge-keyed sign dict; a +-1 sequence) would fail this "
                 "probe; shapes outside those two are not scanned -- see "
                 "the disclosures"})

    # the S2 Case-A collapse as positive control: constant labels ->
    # trivial character on EVERY configuration at stated n
    total = 0
    with_cycles = 0
    ok = True
    bell_sum = sum(_bell(n) for n in (3, 4, 5))
    for n in (3, 4, 5):
        for P in _set_partitions(n):
            total += 1
            E = _sep_edges(P, n)
            idx = {e: k for k, e in enumerate(E)}
            basis = _fundamental_cycles(list(range(n)), E)
            if basis:
                with_cycles += 1
            const = (1,) * len(E)
            ok &= (holonomy_character(const, idx, basis)
                   == (1,) * len(basis))
    legs["case_a_constant_labels_trivial_character"] = (
        ok and total == bell_sum and total == 72 and with_cycles > 0,
        {"configurations": total, "bell_3_to_5_sum": bell_sum,
         "configurations_with_nonempty_cycle_space": with_cycles,
         "note": "the S2 Case-A collapse run as a positive control: the "
                 "constant-label network returns the trivial character on "
                 "every configuration at n = 3..5",
         "labels": _LABELS_IMPORTED})

    return _result(
        "check_J5_supply_slot_open", legs,
        key_result=(
            f"The label slot is open and explicit: the {len(found)} "
            f"label-consuming functions take `labels` as their first "
            f"parameter (set-exact), no module-level constant of either "
            f"scanned shape (edge-keyed sign dict; +-1 sequence) supplies "
            f"edge labels, and the constant-label network returns the trivial "
            f"character on all {total} configurations at n = 3..5 (the S2 "
            f"Case-A positive control).  What supplies lambda_S per "
            f"configuration is NOT computed here; the one live candidate "
            f"type -- the A12-weakened cycle-space-valued occupancy count "
            f"over QAC input -- is named here with its identification "
            f"obligation, and built nowhere."),
        cross_refs=[],
        disclosures=[
            "what the two probes compute: the declared consumer list is "
            "set-exact against the module's own functions, and no "
            "module-level constant of either scanned shape (edge-keyed "
            "sign dict; +-1 sequence) exists.  What they cannot certify: "
            "the absence of a label supplier in any other shape.  Three "
            "demonstrated evading shapes (each evades these probes -- "
            "added to a scratch copy during the blinded audits, the J5 "
            "legs stayed green): a "
            "module-level function computing labels from (n, P); a "
            "check-local closure; a module-level configuration-keyed "
            "lookup table.  That residual is a stated limitation: no "
            "probe in this module reaches it; it is left to audits of "
            "the source",
            "the live candidate type is the A12-weakened cycle-space-"
            "valued occupancy count over QAC input; its identification "
            "obligation (a demonstration that the class the represented "
            "side measures IS the character such a function returns) is "
            "named; nothing here constructs, approximates, or selects it"])


# ---------------------------------------------------------------------------
# module surface -- registration (BARE-NAME keys per D6@2026-08-03)
# ---------------------------------------------------------------------------

_CHECKS = {
    "check_J1_sep_network_cycle_space": check_J1_sep_network_cycle_space,
    "check_J2_z2_composition_canonical": check_J2_z2_composition_canonical,
    "check_J3_class_character_bijection":
        check_J3_class_character_bijection,
    "check_J4_enrichment_controls": check_J4_enrichment_controls,
    "check_J5_supply_slot_open": check_J5_supply_slot_open,
}


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


def register(registry):
    registry.update({
        "J1_sep_network_cycle_space": check_J1_sep_network_cycle_space,
        "J2_z2_composition_canonical": check_J2_z2_composition_canonical,
        "J3_class_character_bijection": check_J3_class_character_bijection,
        "J4_enrichment_controls": check_J4_enrichment_controls,
        "J5_supply_slot_open": check_J5_supply_slot_open,
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
