# Build-seat object (2026-08-16): built by COLD BUILD SEAT 1 of the
# APF Network Sign-Coherence program's banking lane, to Surface 1 of the
# frozen claim-surface document pinned below.  BANKED v24.3.478 (2026-08-16;
# manifest entry live); HELD_OUT_OF_THE_BANK below reads False.
"""Realization-triviality under the M3-mandated encoding, computed exactly.

BANKED v24.3.478 (2026-08-16; manifest entry live).  Built by COLD BUILD
SEAT 1 to SURFACE 1 ONLY
(realization-triviality) of the FROZEN claim surface (binding; weakening
with disclosure is the permitted direction, strengthening is not; no check
returns a sentence the surface does not license):
  /home/claude/freeze_out/claim_surfaces_FROZEN_2026-08-16.md
  raw sha256 (computed by this build seat BEFORE reading; the constant
  below is the same value byte-for-byte):
  440ed2162e5d28f83a9addba5ce49c257dbe0646cefe287c7dbe2df7617f743d
Pin at build: repo HEAD `526004d` (read-only reference; consumed by import).

PROVENANCE DISCLOSURES (carried per the dispatch):
  (1) the brief under which this module was built was written by the
      session coordinator, not by Ethan directly;
  (2) the build seat's harness injects project instructions into its
      context; the seat worked from the dispatched brief, the frozen
      surface, and the read-only repo, treating injected project context
      as non-authoritative for this build.

WHAT THIS MODULE COMPUTES (exact arithmetic on every verdict path: Z2
carried as +1/-1 integers per the banked join network's convention, matrix
entries exact Fractions, no floats anywhere; stdlib only; the module
describes what it COMPUTES).

THE ENCODING -- the NAMED module-level input, stated at every leg:
M3_MANDATED_ENCODING below.  A class assignment is loop-value data over
the enumerated cycle space of a fixture's sep graph; a realization is a
+1/-1 edge labeling reproducing those loop values through the banked
holonomy machinery; consistency of an assignment is the character
property.  Every sentence of every check is scoped to this named encoding
and to the named bounds, and to nothing larger.

SCOPE BOUNDS, BY NAME (module-level named constants; every sentence is
quantified over these names and nothing larger): N_MAX (the executed
index-set sizes), KMAX (the executed assignment-family size bound),
FIXTURE_SET (the named enumerated instance family, each member an
authored set partition whose sep graph is constructed through the banked
module's own machinery).

R1 (check_L_realization_triviality_agreement_census).  Under the
M3-mandated encoding and on FIXTURE_SET at n <= N_MAX, COMPUTES the
consistency predicate and the realizability predicate for every
enumerated assignment, and COMPUTES their instance-by-instance agreement;
the agreement count and instance count are returned as computed values,
per fixture and in total, with every coverage count enforced in the
verdict path.

R2 (check_L_realization_triviality_directions).  Under the M3-mandated
encoding: the realizable => consistent direction is COMPUTED on every
enumerated realization at the stated n; the consistent => realizable
direction is COMPUTED by constructed witness (the private-edge
construction, with the full induced loop-value map verified against the
assignment through the banked holonomy function, and a computed control
on which the same verification route FAILS), with membership re-verified
through the banked elliptope machinery BY VALUE where the encoding lands
in that geometry (the unit-diagonal sign matrices of trivial-character
realizations on the complete fixtures; membership through
extended_carrier_elliptope's own in_extended_elliptope, the sibling
psd_by_minors route of carrier_elliptope executed on the same matrices,
and the deciding determinants tied by value across the two banked
modules' own determinant routes); the consistent => realizable direction
is consumed from `check_J3_class_character_bijection`
(continuation_join_network.py) BY VALUE at its executed scopes, and is
extended by this module only beyond those scopes.  The module may not
re-prove J3's content where scopes meet -- and does not: no call to the
banked switching-class machinery appears in this file (a computed
exact-token source census records the absence at the census's own stated
scope, at the leg).

R3 (check_L_contextual_encoding_control).  One executed control exhibits
a NAMED alternative encoding (ALT_ENCODING_CONTEXTUAL_FIRST_EDGE below: a
per-leg contextual read -- the loop value read off one designated leg of
the loop rather than the Z2 product over the loop) on which the computed
agreement FAILS on the named control fixture, so the encoding-scope
clause is load-bearing, computed -- under the M3-mandated encoding only.

R4 (check_L_rank_one_adjacency_value_tie).  Where the encoding's
realizations meet banked objects, the meeting is a VALUE TIE through the
banked module's own functions: `check_L_rank_one_achievement`
(extended_carrier_elliptope.py) is executed live and its returned
computed completion counts are tied by value against this module's
computed trivial-character realization count on the matching fixture --
disclosed as a tie of computed counts between DIFFERENT objects, never an
identification (adjacency is not identification, the standing fence;
equally, nothing here supersedes that banked check).

LEG INVENTORY (D7@2026-08-08, APPEND-AND-RECORD): _result() compares the
executed leg set against EXPECTED_LEGS set-exactly on the path a run
would execute; a mismatch contributes a failure reason and does not
raise.  STANDING LIMIT, disclosed: this certifies that a declared leg
EXECUTED, not that it COULD HAVE FAILED; a computed verdict replaced by a
constant escapes it, as it escapes the raising form equally.

AUTHORED INPUTS (disclosed, not discharged): the FIXTURE_SET partitions,
N_MAX, KMAX, the control-fixture choice, the alternative encoding's read
rule, the witness construction's private-edge choice rule, and the
inconsistent-control flip site.  What the module computes, it computes
GIVEN these inputs.

DISCLOSED IDENTITY-GRADE LEGS (battery genre): the cross-module
determinant tie in R2 pins agreement of two independently housed cofactor
routes (the EE2 precedent -- route agreement, not a fact about nature);
the cyclomatic count tie in R1 (basis size against m - n + c through the
banked component counter) re-executes the banked J1 identity on this
module's fixtures.  The falsifiable content of the elliptope leg is the
membership verdict pattern and its computed non-vacuity controls.

DISCLOSED RESIDUALS: (1) the exact-token census in R2 is a scan of this
file for one token spelling; a re-derivation under a different spelling
is outside its reach (stated at the leg).  (2) The alternative encoding
is one authored control; the census of alternative encodings is not
exhausted and no sentence claims it is.  (3) The witness construction's
edge choice is authored; existence claims are exactly as strong as the
executed witness, and no uniqueness is computed or claimed.

MAY-NOT-CITE: Surface 1's own list, carried in MAY_NOT_CITE
below, and the header's standing fences, carried in
STANDING_FENCES below; both returned in every record.
"""

import os
from fractions import Fraction as F
from itertools import combinations, product

from apf import continuation_join_network as _cjn
from apf import extended_carrier_elliptope as _ee
from apf import carrier_elliptope as _cee

HELD_OUT_OF_THE_BANK = False  # BANKED v24.3.478 (2026-08-16); landing rewire disclosed in the manifest

CLAIM_SURFACE_SHA256 = (
    "440ed2162e5d28f83a9addba5ce49c257dbe0646cefe287c7dbe2df7617f743d")

# ---------------------------------------------------------------------------
# the encoding -- the NAMED module-level input, stated at every leg
# ---------------------------------------------------------------------------

M3_MANDATED_ENCODING = (
    "M3-mandated encoding (the edge-sign/GF(2) realization), the NAMED "
    "module-level input of every leg: a class assignment is loop-value "
    "data over the enumerated cycle space of the fixture's sep graph -- "
    "one value in {+1, -1} per cycle-space element, the cycle space "
    "enumerated as GF(2) coordinates over the fundamental-cycle basis "
    "computed through continuation_join_network's own _fundamental_cycles; "
    "a realization is a {+1, -1} edge labeling reproducing every loop "
    "value, the loop value of a labeling on an element computed through "
    "continuation_join_network's own holonomy_of_cycle (the Z2 product of "
    "the labels over the element's edges); consistency of an assignment "
    "is the character property: value +1 at the empty element and "
    "multiplicativity over the GF(2) sum on every pair of elements")

ALT_ENCODING_CONTEXTUAL_FIRST_EDGE = (
    "CONTEXTUAL_FIRST_EDGE_READ, the NAMED alternative encoding of the "
    "executed control (per-leg contextual): the loop value of a nonempty "
    "cycle-space element under a labeling is the label of the element's "
    "lexicographically first edge -- a read of one designated leg of the "
    "loop, contextual in that designation -- and +1 at the empty element; "
    "no product over the loop is taken")

# ---------------------------------------------------------------------------
# scope bounds, by name (authored inputs, disclosed)
# ---------------------------------------------------------------------------

N_MAX = 6      # the executed index-set sizes: every fixture has n <= N_MAX
KMAX = 65536   # the executed assignment-family size bound, per fixture

# The named enumerated instance family: (name, n, partition).  Each sep
# graph is CONSTRUCTED through continuation_join_network's own _sep_edges
# on the authored partition; nothing here authors an edge list directly.
FIXTURE_SET = (
    ("K3", 3, ((0,), (1,), (2,))),
    ("K13_n4", 4, ((0,), (1, 2, 3))),
    ("K22_n4", 4, ((0, 1), (2, 3))),
    ("K112_n4", 4, ((0,), (1,), (2, 3))),
    ("K4", 4, ((0,), (1,), (2,), (3,))),
    ("K23_n5", 5, ((0, 1), (2, 3, 4))),
    ("K122_n5", 5, ((0,), (1, 2), (3, 4))),
    ("K24_n6", 6, ((0, 1), (2, 3, 4, 5))),
    ("K33_n6", 6, ((0, 1, 2), (3, 4, 5))),
)

CONTROL_FIXTURE = "K4"  # the named fixture of the R3 executed control

# Surface 1's MAY-NOT-CITE list, verbatim (binding; returned in every
# record).
MAY_NOT_CITE = (
    '"consistency and realizability are equivalent" in any sentence not '
    "carrying the encoding-scope clause; any claim at n or family sizes "
    "beyond the named bounds; any supply, read-channel, or formation-map "
    "claim; anything for or against situational-S; "
    "`check_L_rank_one_achievement` or `check_K1_coboundary_kill` as "
    "already containing this theorem (adjacency is not identification), "
    "and equally this module as superseding them; any sentence about what "
    "the encoding prevents.",
)

# The header's standing fences, verbatim (binding on every surface;
# returned in every record).
STANDING_FENCES = (
    '"the transfer is forced" -- negative; may not be claimed.',
    '"the carrier gap is closed / narrowed" -- may not be claimed.',
    '"Born is derived" without its conditional clause -- may not be '
    "claimed.",
    "The O2 close and the OT3 vacuity ruling are quotable only whole.",
    "ORIENTATION_COVER_REALIZED is uncertified.",
    "The Paper 9 ladder is not banked.",
    "record_coherence_tradeoff is never a supply.",
    "The banked join network supplies no sign.",
    "Adjacency is not identification.",
)

EXPECTED_LEGS = {
    "check_L_realization_triviality_agreement_census": [
        "agreement_counts_enforced_and_returned",
        "consistency_predicate_computed_on_every_assignment",
        "fixture_inventory_bounds_and_dims_enforced",
        "realizability_predicate_computed_on_every_assignment",
    ],
    "check_L_realization_triviality_directions": [
        "consistent_implies_realizable_constructed_witness_verified",
        "elliptope_membership_reverified_where_encoding_lands",
        "extension_beyond_j3_executed_scope_computed",
        "j3_direction_consumed_by_value_at_executed_scopes",
        "realizable_implies_consistent_on_every_enumerated_realization",
        "witness_verification_fails_on_inconsistent_control",
    ],
    "check_L_contextual_encoding_control": [
        "agreement_fails_under_alternative_encoding",
        "alternative_encoding_named_and_differs_by_value",
        "m3_agreement_total_on_control_fixture",
        "realizable_implies_consistent_breaks_under_alternative",
    ],
    "check_L_rank_one_adjacency_value_tie": [
        "ee_check_executed_live_and_passed",
        "trivial_class_count_tied_to_ee_completion_count_by_value",
    ],
}

_ENC = "encoding: M3_MANDATED_ENCODING (the named module-level input)"


# ---------------------------------------------------------------------------
# result plumbing (append-and-record leg inventory, sited in the per-check
# result assembly -- D7@2026-08-08)
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
        "genre_note": (
            "a consistency/realizability agreement census under the "
            "M3-mandated encoding, on FIXTURE_SET at n <= N_MAX with the "
            "assignment family bounded by KMAX; every sentence is scoped "
            "to the named encoding and the named bounds; nothing physical "
            "is claimed, no supply is claimed, and no sentence is about "
            "what the encoding prevents"),
        "encoding": M3_MANDATED_ENCODING,
        "scope_bounds": {
            "N_MAX": N_MAX,
            "KMAX": KMAX,
            "FIXTURE_SET": [nm for nm, _n, _P in FIXTURE_SET],
        },
        "legs": {k: {"passed": bool(v[0]), "evidence": v[1]}
                 for k, v in legs.items()},
        "leg_count": len(legs),
        "fail_reasons": fails,
        "key_result": key_result,
        "conditional_on": [
            "the banked continuation_join_network machinery "
            "(_sep_edges, _components, _fundamental_cycles, "
            "holonomy_of_cycle) and the banked elliptope machinery "
            "(extended_carrier_elliptope, carrier_elliptope), consumed by "
            "value; their premises and authored inputs are inherited, not "
            "discharged",
        ],
        "authored_inputs": [
            "the FIXTURE_SET partitions", "N_MAX", "KMAX",
            "the control-fixture choice",
            "the alternative encoding's read rule",
            "the witness construction's private-edge choice rule",
            "the inconsistent-control flip site",
        ],
        "dependencies": list(dependencies),
        "cross_refs": list(cross_refs),
        "disclosures": list(disclosures),
        "may_not_cite": list(MAY_NOT_CITE),
        "standing_fences": list(STANDING_FENCES),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "frozen_claim_surface_sha256": CLAIM_SURFACE_SHA256,
        "inventory_note": (
            "append-and-record (D7@2026-08-08): certifies a declared leg "
            "EXECUTED, not that it could have failed"),
    }


# ---------------------------------------------------------------------------
# fixture construction: every graph object through the banked module's own
# machinery (nothing re-implemented); the cycle space enumerated as GF(2)
# coordinates over the banked fundamental-cycle basis
# ---------------------------------------------------------------------------

def _build_fixture(name, n, P):
    edges = _cjn._sep_edges([list(b) for b in P], n)
    m = len(edges)
    c = _cjn._components(list(range(n)), edges)
    basis = _cjn._fundamental_cycles(list(range(n)), edges)
    dim = len(basis)
    eidx = {e: k for k, e in enumerate(edges)}
    kk = 2 ** dim
    elem_edges = []
    elem_bitmask = []
    for mask in range(kk):
        s = frozenset()
        for i in range(dim):
            if mask & (1 << i):
                s = s ^ frozenset(basis[i])
        elem_edges.append(tuple(sorted(s)))
        elem_bitmask.append(sum(1 << eidx[e] for e in s))
    return {
        "name": name, "n": n, "P": P, "edges": edges, "m": m, "c": c,
        "basis": basis, "dim": dim, "eidx": eidx, "kk": kk,
        "elem_edges": elem_edges, "elem_bitmask": elem_bitmask,
        # J3's executed scopes: the Kn arm at its stated n where the
        # fixture is complete, and the complete-multipartite sep-graph
        # extension at n = 4 and n = 5 (>= 2-block partitions) -- the
        # containment is COMPUTED from the fixture data, not authored.
        "in_j3_scope": ((n in (4, 5) and len(P) >= 2)
                        or (n == 3 and m == n * (n - 1) // 2)),
        "complete": m == n * (n - 1) // 2,
    }


_FIXTURES = None


def _fixtures():
    global _FIXTURES
    if _FIXTURES is None:
        _FIXTURES = {name: _build_fixture(name, n, P)
                     for name, n, P in FIXTURE_SET}
    return _FIXTURES


# ---------------------------------------------------------------------------
# the two predicates of the M3-mandated encoding
# ---------------------------------------------------------------------------

def _is_character(Z, kk):
    """The consistency predicate: +1 at the empty element and
    multiplicativity over the GF(2) sum on every pair of elements."""
    if Z[0] != 1:
        return False
    for i in range(kk):
        zi = Z[i]
        for j in range(i, kk):
            if Z[i ^ j] != zi * Z[j]:
                return False
    return True


def _induced_map(labels, fx):
    """The loop-value map a realization induces, computed through the
    banked module's own holonomy function on every cycle-space element."""
    eidx = fx["eidx"]
    return tuple(_cjn.holonomy_of_cycle(labels, eidx, fx["elem_edges"][m])
                 for m in range(fx["kk"]))


def _alt_induced_map(labels, fx):
    """The loop-value map under the NAMED alternative encoding
    (ALT_ENCODING_CONTEXTUAL_FIRST_EDGE): the label of the element's
    lexicographically first edge; +1 at the empty element."""
    eidx = fx["eidx"]
    out = []
    for m in range(fx["kk"]):
        ee = fx["elem_edges"][m]
        out.append(1 if not ee else labels[eidx[min(ee)]])
    return tuple(out)


_CENSUS = None


def _census():
    """The R1 census, computed once: for every fixture, every assignment's
    consistency and realizability verdicts and their agreement, plus the
    achieved-map set over every enumerated realization."""
    global _CENSUS
    if _CENSUS is not None:
        return _CENSUS
    out = {}
    for name, fx in _fixtures().items():
        kk = fx["kk"]
        m = fx["m"]
        achieved = set()
        for labels in product((1, -1), repeat=m):
            achieved.add(_induced_map(labels, fx))
        n_total = 0
        n_cons = 0
        n_real = 0
        n_agree = 0
        cons_list = []
        for Z in product((1, -1), repeat=kk):
            n_total += 1
            cons = _is_character(Z, kk)
            real = Z in achieved
            if cons:
                n_cons += 1
                cons_list.append(Z)
            if real:
                n_real += 1
            if cons == real:
                n_agree += 1
        out[name] = {
            "n_total": n_total, "n_consistent": n_cons,
            "n_realizable": n_real, "n_agree": n_agree,
            "achieved": achieved, "consistent": cons_list,
            "n_labelings": 2 ** m,
        }
    _CENSUS = out
    return out


def _own_source():
    path = os.path.abspath(__file__)
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read(), path


# ---------------------------------------------------------------------------
# R1 -- the agreement census (Surface 1, sentence 1)
# ---------------------------------------------------------------------------

def check_L_realization_triviality_agreement_census():
    legs = {}
    fxs = _fixtures()
    cen = _census()

    n_fx = 0
    ok = len(fxs) == len(FIXTURE_SET) > 0
    dims = {}
    for name, fx in sorted(fxs.items()):
        # bounds enforced: n <= N_MAX; assignment family within KMAX
        if not (fx["n"] <= N_MAX and 2 ** fx["kk"] <= KMAX):
            ok = False
        # the cyclomatic tie, re-executed on this fixture through the
        # banked component counter: |basis| = m - n + c (identity genre,
        # disclosed: J1's banked identity re-executed here as a gate)
        if fx["dim"] != fx["m"] - fx["n"] + fx["c"]:
            ok = False
        # basis independence: the enumerated cycle-space elements are
        # pairwise distinct as edge sets
        if len(set(fx["elem_bitmask"])) != fx["kk"]:
            ok = False
        dims[name] = fx["dim"]
        n_fx += 1
    ok = ok and n_fx == len(FIXTURE_SET)
    legs["fixture_inventory_bounds_and_dims_enforced"] = (ok, (
        f"{_ENC}; FIXTURE_SET carries {n_fx} named fixtures (count "
        f"enforced against the declared tuple), every sep graph "
        f"constructed through continuation_join_network's own _sep_edges "
        f"on the authored partition, every "
        f"n <= N_MAX = {N_MAX} and every assignment-family size "
        f"2^(2^dim) <= KMAX = {KMAX} enforced; per-fixture cycle-space "
        f"dims computed as |basis| through the banked _fundamental_cycles "
        f"and tied to m - n + c through the banked _components (identity "
        f"genre, disclosed: the banked J1 cyclomatic identity re-executed "
        f"on these fixtures as a gate); enumerated cycle-space elements "
        f"pairwise distinct as edge sets, enforced; dims: {dims}"))

    n_tot = 0
    n_cons = 0
    ok = True
    for name, fx in sorted(fxs.items()):
        row = cen[name]
        if row["n_total"] != 2 ** fx["kk"]:
            ok = False
        # the character count of a GF(2) cycle space of the computed dim,
        # enforced as a computed coverage count
        if row["n_consistent"] != 2 ** fx["dim"]:
            ok = False
        n_tot += row["n_total"]
        n_cons += row["n_consistent"]
    legs["consistency_predicate_computed_on_every_assignment"] = (ok, (
        f"{_ENC}; the consistency predicate (the character property: +1 "
        f"at the empty element, multiplicativity over the GF(2) sum on "
        f"every pair of elements) computed on every enumerated assignment "
        f"of every fixture -- {n_tot} assignments in total (per-fixture "
        f"totals enforced equal to 2^(2^dim)); the computed consistent "
        f"count per fixture is enforced equal to 2^dim, {n_cons} "
        f"consistent assignments in total"))

    n_real = 0
    n_lab = 0
    ok = True
    for name, fx in sorted(fxs.items()):
        row = cen[name]
        if row["n_realizable"] != len(row["achieved"]):
            ok = False
        if row["n_labelings"] != 2 ** fx["m"]:
            ok = False
        n_real += row["n_realizable"]
        n_lab += row["n_labelings"]
    legs["realizability_predicate_computed_on_every_assignment"] = (ok, (
        f"{_ENC}; the realizability predicate computed on every "
        f"enumerated assignment by membership in the achieved-map set: "
        f"every one of the {n_lab} enumerated realizations (per-fixture "
        f"counts enforced equal to 2^m) induces its full loop-value map "
        f"through continuation_join_network's own holonomy_of_cycle, and "
        f"an assignment is realizable exactly when it equals an induced "
        f"map; the realizable count per fixture is enforced equal to the "
        f"achieved-set size, {n_real} realizable assignments in total"))

    rows = {}
    n_agree = 0
    ok = True
    for name, fx in sorted(fxs.items()):
        row = cen[name]
        if row["n_agree"] != row["n_total"]:
            ok = False
        if row["n_consistent"] != row["n_realizable"]:
            ok = False
        rows[name] = (f"agree {row['n_agree']} / total {row['n_total']} "
                      f"(consistent {row['n_consistent']}, realizable "
                      f"{row['n_realizable']})")
        n_agree += row["n_agree"]
    ok = ok and n_agree == n_tot
    legs["agreement_counts_enforced_and_returned"] = (ok, (
        f"{_ENC}; the instance-by-instance agreement of the two computed "
        f"predicates: per fixture the agreement count is ENFORCED equal "
        f"to the instance count and the consistent and realizable counts "
        f"are enforced equal, and the totals tie ({n_agree} agreements "
        f"over {n_tot} enumerated assignments, enforced); per-fixture "
        f"computed rows: {rows}"))

    return _result(
        "check_L_realization_triviality_agreement_census", legs,
        key_result=(
            f"under the M3-mandated encoding (the encoding a NAMED "
            f"module-level input, stated at every leg) and on FIXTURE_SET "
            f"at n <= N_MAX = {N_MAX}, this module COMPUTES the "
            f"consistency predicate and the realizability predicate for "
            f"every enumerated assignment, and COMPUTES their "
            f"instance-by-instance agreement; the agreement count and "
            f"instance count are returned as computed values: "
            f"{n_agree} agreements over {n_tot} enumerated assignments "
            f"across {n_fx} fixtures, every coverage count enforced; "
            f"nothing at n or family sizes beyond the named bounds is "
            f"claimed"),
        dependencies=["T_continuation_join_network_J1",
                      "T_continuation_join_network_J3"],
        cross_refs=["check_L_realization_triviality_directions"],
        disclosures=[
            "the cyclomatic count tie is a disclosed identity-grade gate "
            "(the banked J1 identity re-executed on these fixtures)",
            "the FIXTURE_SET partitions and both bounds are authored "
            "inputs, disclosed, not discharged"])


# ---------------------------------------------------------------------------
# R2 -- the two directions and the geometry re-verification
# (Surface 1, sentence 2, with Ethan's ruled amendment carried)
# ---------------------------------------------------------------------------

def check_L_realization_triviality_directions():
    legs = {}
    fxs = _fixtures()
    cen = _census()

    # realizable => consistent, computed on every enumerated realization
    n_checked = 0
    ok = True
    for name, fx in sorted(fxs.items()):
        for labels in product((1, -1), repeat=fx["m"]):
            if not _is_character(_induced_map(labels, fx), fx["kk"]):
                ok = False
            n_checked += 1
    want = sum(2 ** fx["m"] for fx in fxs.values())
    ok = ok and n_checked == want > 0
    legs["realizable_implies_consistent_on_every_enumerated_realization"] = (
        ok, (
            f"{_ENC}; the realizable => consistent direction COMPUTED on "
            f"every enumerated realization at the stated n: each of the "
            f"{n_checked} realizations (count enforced equal to the "
            f"summed 2^m over FIXTURE_SET, nonempty) induces its full "
            f"loop-value map through the banked holonomy_of_cycle, and "
            f"the map passes the consistency predicate -- computed, this "
            f"module's own direction at every fixture"))

    # consistent => realizable, computed by constructed witness
    n_wit = 0
    ok = True
    for name, fx in sorted(fxs.items()):
        dim = fx["dim"]
        basis = fx["basis"]
        # the private-edge choice: for each basis cycle, an edge lying in
        # no other basis cycle (nonempty enforced; choice authored)
        private = []
        for i in range(dim):
            others = set()
            for j in range(dim):
                if j != i:
                    others |= set(basis[j])
            cand = [e for e in basis[i] if e not in others]
            if not cand:
                ok = False
            private.append(min(cand) if cand else None)
        for Z in cen[name]["consistent"]:
            labels = [1] * fx["m"]
            for i in range(dim):
                if Z[1 << i] == -1:
                    labels[fx["eidx"][private[i]]] = -1
            if _induced_map(tuple(labels), fx) != Z:
                ok = False
            n_wit += 1
    want_wit = sum(2 ** fx["dim"] for fx in fxs.values())
    ok = ok and n_wit == want_wit > 0
    legs["consistent_implies_realizable_constructed_witness_verified"] = (
        ok, (
            f"{_ENC}; the consistent => realizable direction COMPUTED by "
            f"constructed witness on every consistent assignment of every "
            f"fixture ({n_wit} witnesses, count enforced equal to the "
            f"summed 2^dim): the witness sets every label +1 and flips "
            f"the private edge of each basis cycle whose assigned value "
            f"is -1 (private edges computed, nonemptiness enforced; the "
            f"choice rule authored, disclosed), and the witness's FULL "
            f"induced loop-value map -- every cycle-space element, "
            f"through the banked holonomy_of_cycle -- is verified equal "
            f"to the assignment; at J3's executed scopes this leg is "
            f"witness EXECUTION under the direction consumed from J3 (see "
            f"the consumption leg), not a re-derivation of J3's "
            f"class-character bijection; beyond those scopes it is this "
            f"module's own extension"))

    # the same verification route FAILS on an exhibited inconsistent
    # assignment (the control that shows the witness leg can fail)
    fx = fxs[CONTROL_FIXTURE]
    base = None
    for Z in cen[CONTROL_FIXTURE]["consistent"]:
        if any(z == -1 for z in Z):
            base = Z
            break
    ok = base is not None and fx["dim"] >= 2
    flip_site = 3  # the GF(2) sum of the first two basis elements (authored)
    zbad = None
    if ok:
        zb = list(base)
        zb[flip_site] = -zb[flip_site]
        zbad = tuple(zb)
        if _is_character(zbad, fx["kk"]):
            ok = False
        basis = fx["basis"]
        private = []
        for i in range(fx["dim"]):
            others = set()
            for j in range(fx["dim"]):
                if j != i:
                    others |= set(basis[j])
            cand = [e for e in basis[i] if e not in others]
            private.append(min(cand))
        labels = [1] * fx["m"]
        for i in range(fx["dim"]):
            if zbad[1 << i] == -1:
                labels[fx["eidx"][private[i]]] = -1
        induced = _induced_map(tuple(labels), fx)
        if induced == zbad:
            ok = False
        if zbad in cen[CONTROL_FIXTURE]["achieved"]:
            ok = False
    legs["witness_verification_fails_on_inconsistent_control"] = (ok, (
        f"{_ENC}; control on the named fixture {CONTROL_FIXTURE}: an "
        f"exhibited assignment built by flipping a consistent "
        f"assignment's value at the element with basis-coordinate mask "
        f"{flip_site} (authored flip site) computes INCONSISTENT, the "
        f"same witness construction's full-map verification FAILS on it "
        f"(computed inequality), and it is absent from the achieved-map "
        f"set (computed) -- the witness-verification route and the "
        f"realizability predicate can both fail, executed"))

    # the ruled amendment: consistent => realizable consumed from J3 BY
    # VALUE at its executed scopes; extended only beyond them
    rec = _cjn.check_J3_class_character_bijection()
    ok = rec.get("passed") is True
    rows = rec["legs"]["kn_switching_classes_2_8_64_union_find"][
        "evidence"]["rows"]
    ext = rec["legs"]["extension_complete_multipartite_n4_n5"][
        "evidence"]["graphs"]
    ext_passed = rec["legs"]["extension_complete_multipartite_n4_n5"][
        "passed"]
    surj_passed = rec["legs"]["character_surjective_onto_z2_dim"]["passed"]
    ok = ok and ext_passed and surj_passed
    ties = []
    # Kn-arm value ties: this module's computed consistent counts and
    # dims against J3's returned computed rows, for the complete fixtures
    # at J3's stated n
    for name in ("K3", "K4"):
        fx2 = fxs[name]
        row = rows[str(fx2["n"])]
        t1 = (cen[name]["n_consistent"] == row["distinct_characters"])
        t2 = (fx2["dim"] == row["dim"])
        ok = ok and t1 and t2 and fx2["complete"]
        ties.append(f"{name}: consistent {cen[name]['n_consistent']} == "
                    f"J3 distinct_characters {row['distinct_characters']}, "
                    f"dim {fx2['dim']} == J3 dim {row['dim']}")
    # extension-arm value ties: J3's returned per-n graph counts against
    # the banked Bell counter, and computed scope containment of every
    # in-scope fixture
    for nn in (4, 5):
        t = (int(ext[str(nn)]) == _cjn._bell(nn) - 1)
        ok = ok and t
        ties.append(f"J3 ext graph count at n={nn}: {ext[str(nn)]} == "
                    f"Bell({nn}) - 1 = {_cjn._bell(nn) - 1} (through the "
                    f"banked _bell)")
    # computed containment: each in-scope fixture's edge set is a MEMBER
    # of the family J3's extension arm executed (that family re-enumerated
    # through the banked module's own _set_partitions/_sep_edges and its
    # size tied by value to J3's returned graph count), or -- for the
    # complete fixture at J3's smallest stated n -- of J3's Kn arm
    in_scope = sorted(nm for nm, fx2 in fxs.items() if fx2["in_j3_scope"])
    fam_cache = {}
    n_contain = 0
    for nm in in_scope:
        fx2 = fxs[nm]
        if fx2["n"] in (4, 5):
            if fx2["n"] not in fam_cache:
                fam_cache[fx2["n"]] = [
                    _cjn._sep_edges(P, fx2["n"])
                    for P in _cjn._set_partitions(fx2["n"])
                    if len(P) >= 2]
            fam = fam_cache[fx2["n"]]
            if fx2["edges"] not in fam:
                ok = False
            if len(fam) != int(ext[str(fx2["n"])]):
                ok = False
        else:
            if not (str(fx2["n"]) in rows and fx2["complete"]):
                ok = False
        n_contain += 1
    ok = ok and n_contain == len(in_scope) > 0
    # the no-re-proof census: this module's source carries no call to the
    # switching-class machinery (exact-token scan; census scope stated)
    src, path = _own_source()
    token = "_switching" + "_classes("
    ok = ok and (token not in src)
    legs["j3_direction_consumed_by_value_at_executed_scopes"] = (ok, (
        f"{_ENC}; the consistent => realizable direction is CONSUMED from "
        f"check_J3_class_character_bijection (continuation_join_network) "
        f"BY VALUE at its executed scopes (Ethan's ruled amendment, "
        f"2026-08-16, carried): the banked check is executed live and "
        f"passed; its returned computed counts are tied by value -- "
        f"{ties} -- and every in-scope fixture's containment in J3's "
        f"executed families is COMPUTED ({n_contain} containments over "
        f"the computed in-scope set {in_scope}, enforced: membership of "
        f"the fixture's edge set in the extension family re-enumerated "
        f"through the banked _set_partitions/_sep_edges with the family "
        f"size tied by value to J3's returned graph count, or the Kn-arm "
        f"row at the fixture's computed-complete n); the module does not "
        f"re-prove J3's content where scopes meet: no call to the banked "
        f"switching-class machinery appears in this file, recorded by an "
        f"exact-token scan of this file "
        f"({path}) for the split-token CALL spelling of the banked "
        f"switching-class machinery (census scope: this one call token in "
        f"this one file; a call under another spelling, or a "
        f"re-implementation, is outside this census's reach, a stated "
        f"limitation)"))

    beyond = sorted(nm for nm, fx2 in fxs.items() if not fx2["in_j3_scope"])
    n_bey = 0
    ok = len(beyond) > 0
    for nm in beyond:
        fx2 = fxs[nm]
        if not fx2["n"] > 5:
            ok = False
        if not (cen[nm]["n_agree"] == cen[nm]["n_total"]):
            ok = False
        n_bey += 1
    ok = ok and n_bey == len(beyond)
    legs["extension_beyond_j3_executed_scope_computed"] = (ok, (
        f"{_ENC}; the extension beyond J3's executed scopes, named and "
        f"computed: the fixtures {beyond} have n computed strictly above "
        f"J3's executed n (enforced per fixture, {n_bey} fixtures); on "
        f"them the consistent => realizable direction rests on this "
        f"module's constructed witnesses and exhaustive verification "
        f"ONLY (the witness leg covers them; agreement equal to total "
        f"re-enforced here per fixture) -- this module extends the "
        f"direction only beyond J3's scopes, and only this far"))

    # elliptope re-verification where the encoding lands in the geometry
    complete = sorted(nm for nm, fx2 in fxs.items() if fx2["complete"])
    ok = len(complete) > 0
    n_triv = 0
    n_ties = 0
    n_fail_ee = 0
    n_fail_cee = 0
    n_nontriv = 0
    triv_counts = {}
    for nm in complete:
        fx2 = fxs[nm]
        n = fx2["n"]
        unit = tuple(F(1) for _ in range(n))
        cnt = 0
        for labels in product((1, -1), repeat=fx2["m"]):
            ind = _induced_map(labels, fx2)
            M = [[F(1) if i == j
                  else F(labels[fx2["eidx"][(min(i, j), max(i, j))]])
                  for j in range(n)] for i in range(n)]
            if all(v == 1 for v in ind):
                cnt += 1
                if not _ee.in_extended_elliptope(M, unit):
                    ok = False
                if not _cee.psd_by_minors(M):
                    ok = False
                if _ee.matrix_rank(M) != 1:
                    ok = False
                # deciding determinants tied by value across the two
                # banked modules' own determinant routes
                for r in range(1, n + 1):
                    for S in combinations(range(n), r):
                        v1 = _ee.det(_ee.submatrix(M, S))
                        v2 = _cee.det_exact(
                            [[M[a][b] for b in S] for a in S])
                        if v1 != v2:
                            ok = False
                        n_ties += 1
            else:
                n_nontriv += 1
                if not _ee.in_extended_elliptope(M, unit):
                    n_fail_ee += 1
                if not _cee.psd_by_minors(M):
                    n_fail_cee += 1
        triv_counts[nm] = cnt
        if cnt != 2 ** (n - 1):
            ok = False
        n_triv += cnt
    ok = (ok and n_fail_ee >= 1 and n_fail_cee >= 1
          and n_ties == sum(triv_counts[nm]
                            * (2 ** fxs[nm]["n"] - 1) for nm in complete))
    legs["elliptope_membership_reverified_where_encoding_lands"] = (ok, (
        f"{_ENC}; where the encoding lands in the banked elliptope "
        f"geometry -- the unit-diagonal sign matrix of a realization is "
        f"defined exactly on the computed complete fixtures {complete} "
        f"(one label per vertex pair) -- membership is re-verified "
        f"through the banked machinery BY VALUE: every trivial-character "
        f"realization's sign matrix ({n_triv} matrices; per-fixture "
        f"counts {triv_counts}, each enforced equal to 2^(n-1)) passes "
        f"extended_carrier_elliptope's own in_extended_elliptope at the "
        f"unit diagonal AND carrier_elliptope's own psd_by_minors, with "
        f"rank computed 1 through the banked matrix_rank and every "
        f"deciding principal determinant tied by value across the two "
        f"banked modules' own determinant routes ({n_ties} ties, count "
        f"enforced; DISCLOSED identity genre: route agreement of two "
        f"banked cofactor determinants, the EE2 precedent); executed "
        f"non-vacuity controls: among the "
        f"nontrivial-character realizations, {n_fail_ee} fail the banked "
        f"membership and {n_fail_cee} fail the sibling route (each "
        f"enforced nonzero, computed) -- the membership verdict pattern "
        f"is the falsifiable content"))

    return _result(
        "check_L_realization_triviality_directions", legs,
        key_result=(
            f"under the M3-mandated encoding, the realizable => "
            f"consistent direction is COMPUTED on every enumerated "
            f"realization at the stated n ({n_checked} realizations, "
            f"enforced); the consistent => realizable direction is "
            f"COMPUTED by constructed witness ({n_wit} witnesses, "
            f"enforced, with an executed failing control), with "
            f"membership re-verified through the banked elliptope "
            f"machinery BY VALUE where the encoding lands in that "
            f"geometry ({n_triv} trivial-character sign matrices on the "
            f"computed complete fixtures); the consistent => realizable "
            f"direction is consumed from check_J3_class_character_"
            f"bijection (continuation_join_network.py) BY VALUE at its "
            f"executed scopes, and is extended by this module only "
            f"beyond those scopes ({beyond}); the module does not "
            f"re-prove J3's content where scopes meet"),
        dependencies=["T_continuation_join_network_J3",
                      "T_extended_carrier_elliptope",
                      "L_rank_one_achievement",
                      "T_carrier_consistent_functionals_are_elliptope"],
        cross_refs=["check_L_realization_triviality_agreement_census",
                    "check_L_rank_one_adjacency_value_tie"],
        disclosures=[
            "the witness construction's private-edge choice rule and the "
            "inconsistent-control flip site are authored inputs",
            "the cross-module determinant tie is a disclosed "
            "identity-grade route agreement (the EE2 precedent); the "
            "membership verdict pattern is the falsifiable content",
            "the no-re-proof census is an exact-token scan of this file "
            "only; a re-derivation under another spelling is outside its "
            "reach (stated limitation)"])


# ---------------------------------------------------------------------------
# R3 -- the named alternative (per-leg contextual) encoding control
# (Surface 1, sentence 3)
# ---------------------------------------------------------------------------

def check_L_contextual_encoding_control():
    legs = {}
    fx = _fixtures()[CONTROL_FIXTURE]
    cen = _census()[CONTROL_FIXTURE]
    kk = fx["kk"]

    # the alternative encoding differs from the M3 encoding by value
    diff = None
    for labels in product((1, -1), repeat=fx["m"]):
        m3 = _induced_map(labels, fx)
        alt = _alt_induced_map(labels, fx)
        if m3 != alt:
            site = next(i for i in range(kk) if m3[i] != alt[i])
            diff = (labels, site, m3[site], alt[site])
            break
    ok = diff is not None
    legs["alternative_encoding_named_and_differs_by_value"] = (ok, (
        f"{_ENC}; the executed control's encoding is the NAMED "
        f"alternative ALT_ENCODING_CONTEXTUAL_FIRST_EDGE (per-leg "
        f"contextual: the loop value is read off the element's "
        f"lexicographically first edge -- one designated leg of the loop "
        f"-- not the Z2 product over the loop); non-vacuity computed on "
        f"the named fixture {CONTROL_FIXTURE}: at labeling "
        f"{diff[0] if diff else None} and cycle-space element mask "
        f"{diff[1] if diff else None}, the M3 loop value computes to "
        f"{diff[2] if diff else None} and the alternative read to "
        f"{diff[3] if diff else None} -- the two encodings differ by "
        f"value"))

    alt_achieved = set()
    for labels in product((1, -1), repeat=fx["m"]):
        alt_achieved.add(_alt_induced_map(labels, fx))
    n_total = 0
    n_agree_alt = 0
    n_real_incons = 0
    n_cons_unreal = 0
    for Z in product((1, -1), repeat=kk):
        n_total += 1
        cons = _is_character(Z, kk)
        real_alt = Z in alt_achieved
        if cons == real_alt:
            n_agree_alt += 1
        elif real_alt and not cons:
            n_real_incons += 1
        else:
            n_cons_unreal += 1
    ok = (n_total == cen["n_total"]
          and n_agree_alt + n_real_incons + n_cons_unreal == n_total
          and n_agree_alt < n_total)
    legs["agreement_fails_under_alternative_encoding"] = (ok, (
        f"{_ENC}; under the named alternative encoding, on the named "
        f"fixture {CONTROL_FIXTURE}: the computed agreement of the "
        f"consistency predicate with alternative-realizability is "
        f"{n_agree_alt} of {n_total} (partition enforced: "
        f"{n_real_incons} alternative-realizable inconsistent "
        f"assignments plus {n_cons_unreal} consistent "
        f"non-alternative-realizable assignments account for every "
        f"disagreement), and the agreement is ENFORCED strictly below "
        f"the instance count -- the computed agreement FAILS under the "
        f"alternative, so the encoding-scope clause is load-bearing, "
        f"computed -- under the M3-mandated encoding only (the surface's "
        f"own sentence; the census of alternative encodings is one "
        f"executed control, not an exhaustion)"))

    all_minus = tuple(-1 for _ in range(fx["m"]))
    amap = _alt_induced_map(all_minus, fx)
    viol = None
    for i in range(kk):
        for j in range(kk):
            if amap[i ^ j] != amap[i] * amap[j]:
                viol = (i, j, i ^ j, amap[i ^ j], amap[i] * amap[j])
                break
        if viol:
            break
    ok = (amap in alt_achieved and not _is_character(amap, kk)
          and viol is not None and n_real_incons >= 1)
    legs["realizable_implies_consistent_breaks_under_alternative"] = (ok, (
        f"{_ENC}; the direction that fails under the alternative, "
        f"witnessed: the all-minus labeling's alternative-induced map is "
        f"alternative-realizable by construction yet INCONSISTENT, with "
        f"a computed multiplicativity violation at element masks "
        f"({viol[0] if viol else None}, {viol[1] if viol else None}) -> "
        f"{viol[2] if viol else None}: the map's value there computes to "
        f"{viol[3] if viol else None} against the product "
        f"{viol[4] if viol else None}; the count of "
        f"alternative-realizable inconsistent assignments is "
        f"{n_real_incons}, enforced nonzero"))

    ok = (cen["n_agree"] == cen["n_total"] == n_total)
    legs["m3_agreement_total_on_control_fixture"] = (ok, (
        f"{_ENC}; on the same named fixture the M3-encoding agreement is "
        f"total ({cen['n_agree']} of {cen['n_total']}, tied to the R1 "
        f"census by value and to this check's instance count), so the "
        f"computed failure above is a property of the alternative "
        f"encoding on this fixture, executed side by side with the "
        f"M3-mandated encoding's computed agreement"))

    return _result(
        "check_L_contextual_encoding_control", legs,
        key_result=(
            f"one executed control exhibits a NAMED alternative encoding "
            f"(ALT_ENCODING_CONTEXTUAL_FIRST_EDGE, per-leg contextual) "
            f"on which the computed agreement FAILS on the named fixture "
            f"{CONTROL_FIXTURE} ({n_agree_alt} of {n_total} against the "
            f"M3 encoding's {cen['n_agree']} of {cen['n_total']}), so "
            f"the encoding-scope clause is load-bearing, computed -- "
            f"under the M3-mandated encoding only"),
        dependencies=["T_continuation_join_network_J3"],
        cross_refs=["check_L_realization_triviality_agreement_census",
                    "check_L_realization_triviality_directions"],
        disclosures=[
            "the alternative encoding is one authored control; the "
            "census of alternative encodings is not exhausted and no "
            "sentence claims it is",
            "the control fixture is an authored choice among the named "
            "fixtures"])


# ---------------------------------------------------------------------------
# R4 -- the check_L_rank_one_achievement adjacency: a value tie, never an
# identification (Surface 1, sentence 4)
# ---------------------------------------------------------------------------

def check_L_rank_one_adjacency_value_tie():
    legs = {}
    fxs = _fixtures()

    rec = _ee.check_L_rank_one_achievement()
    kr = rec.get("key_result", {})
    dc = list(kr.get("distinct_completions_per_family", []))
    fam = list(kr.get("families", []))
    ok = (rec.get("passed") is True and len(dc) >= 1
          and len(fam) == len(dc))
    legs["ee_check_executed_live_and_passed"] = (ok, (
        f"{_ENC}; check_L_rank_one_achievement "
        f"(extended_carrier_elliptope) executed live and passed, its "
        f"returned record consumed by value: families {fam}, distinct "
        f"completions per family {dc}, sign vectors iterated "
        f"{kr.get('sign_vectors_iterated')}, equalities checked "
        f"{kr.get('equalities_checked')}"))

    # this module's matching computed count: trivial-character
    # realizations of the complete fixture whose index-set size equals
    # the EE families' size (computed match, not assumed)
    nn = len(fam[0]) if fam else 0
    match = sorted(nm for nm, fx in fxs.items()
                   if fx["complete"] and fx["n"] == nn)
    ok = len(match) >= 1 and all(len(f) == nn for f in fam)
    n_triv = None
    if match:
        fx = fxs[match[0]]
        cnt = 0
        for labels in product((1, -1), repeat=fx["m"]):
            if all(v == 1 for v in _induced_map(labels, fx)):
                cnt += 1
        n_triv = cnt
        for entry in dc:
            if entry != cnt:
                ok = False
        if cnt != 2 ** (nn - 1):
            ok = False
    legs["trivial_class_count_tied_to_ee_completion_count_by_value"] = (
        ok, (
            f"{_ENC}; the VALUE TIE: this module's computed count of "
            f"trivial-character realizations on the fixture "
            f"{match[0] if match else None} (index-set size computed "
            f"equal to the EE families' size {nn}) is {n_triv}, and it "
            f"ties every entry of the banked check's returned "
            f"distinct-completion counts {dc} by value, both sides "
            f"landing on the computed closed form 2^(n-1) at the shared "
            f"n -- a tie of computed quantities through the banked "
            f"module's own executed record; DISCLOSED as a tie and "
            f"nothing more: the banked check's objects are rank-one PSD "
            f"completions at its own matched non-unit diagonals, this "
            f"module's objects are trivial-character edge labelings of a "
            f"named fixture, NO map between them is constructed, and the "
            f"tie is never an identification (adjacency is not "
            f"identification, the standing fence); neither module "
            f"supersedes the other"))

    return _result(
        "check_L_rank_one_adjacency_value_tie", legs,
        key_result=(
            f"where the encoding's realizations meet banked objects, the "
            f"meeting is a value tie through the banked module's own "
            f"functions (the check_L_rank_one_achievement genre): the "
            f"banked check executed live, its returned completion counts "
            f"{dc} tied by value to this module's computed "
            f"trivial-character realization count {n_triv} at the shared "
            f"index-set size -- disclosed as a tie, never an "
            f"identification"),
        dependencies=["L_rank_one_achievement"],
        cross_refs=["check_L_realization_triviality_directions"],
        disclosures=[
            "the tie is between computed counts of DIFFERENT objects; no "
            "identification is constructed and none may be cited",
            "the banked check's grade and scope are its own; this module "
            "carries them as returned, not re-derived"])


# ---------------------------------------------------------------------------
# check table + register() (bare-name keys per D6@2026-08-03) + standalone
# execution.  Banked v24.3.478; the manifest entry is live.
# ---------------------------------------------------------------------------

_CHECKS = {
    "L_realization_triviality_agreement_census":
        check_L_realization_triviality_agreement_census,
    "L_realization_triviality_directions":
        check_L_realization_triviality_directions,
    "L_contextual_encoding_control":
        check_L_contextual_encoding_control,
    "L_rank_one_adjacency_value_tie":
        check_L_rank_one_adjacency_value_tie,
}


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


def register(registry):
    registry.update(_CHECKS)
    return registry


if __name__ == "__main__":
    import sys
    results = run_all()
    n_pass = sum(1 for r in results.values() if r["passed"])
    n_legs = sum(r["leg_count"] for r in results.values())
    print("realization_triviality: BANKED v24.3.478 (2026-08-16); "
          "NOTHING BANKS WITHOUT ETHAN'S LIFT")
    print(f"frozen surface sha256: {CLAIM_SURFACE_SHA256}")
    for name, r in results.items():
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status}] {name} ({r['leg_count']} legs)")
        for reason in r["fail_reasons"]:
            print(f"      FAIL: {reason}")
    print(f"{n_pass}/{len(results)} checks pass; {n_legs} legs")
    sys.exit(0 if n_pass == len(results) else 1)
