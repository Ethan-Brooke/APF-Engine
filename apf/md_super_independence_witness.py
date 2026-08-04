"""Two cost-of-presentation models over the frozen base P: envelope and rank pricing.

Built 2026-08-04 by a cold build seat from
``Artifacts_2026-08-04_session/md_super_independence_build/
BUILD_SPEC_two_model_independence_2026-08-04.md``; parent charter
``Reference - CHARTER - Deriving or Refuting MD-Super-Nodiscount
(2026-08-04)``, Branch N, in the two-model form found by the audit-first
walk.

AUDIT RECORD (all 2026-08-04): audit 1 blinded cold, LAND-WITH-FIXES
0.87; audit 2 blinded cold, LAND-WITH-FIXES 0.88; audit 3 blinded cold,
LAND-WITH-FIXES 0.87; fixes carried by separate cold seats after each
round.  All audits were blinded cold seats under the retired
different-day convention (ruling: ``Reference - DECISION - Retiring the
Different-Day Audit Convention (2026-08-04)``).  Banked as v24.3.466
(2026-08-04).

------------------------------------------------------------------------------
WHAT THIS MODULE COMPUTES (exact arithmetic; stdlib + fractions; shared
machinery imported from the banked v24.3.465 trio, not duplicated)
------------------------------------------------------------------------------

Two cost-of-presentation functionals on real matrices over the complete
uniform carrier K_n, both instances of the SAME argmin construction

    c(x) = eps * min{ k : x = sum_{i=1..k} a_i A_i,
                      A_i in ATOMS, a_i in {+1,-1} },

differing ONLY in the atom set:

  M-ENV  (envelope): ATOMS = the word image = matrix units E_ij.
         Closed form: c_env(x) = eps * |supp(x)| on the signed domain.
         Lower bound: every atom has support size 1, so k atoms cover
         at most k cells (sampled multiset spot-check, plus exhaustive
         brute-force argmin at n = 3, supp <= 2, and 12 sampled supp-3
         cases; the leg names carry the sampling); attainment: the
         cell decomposition, exhaustive on the domains used.  On
         x = e1 E_ab + e2 E_cd (distinct cells) c_env = 2*eps -- the
         no-discount bound holds TIGHT (zero slack, matching the
         md_super sibling's N1 center computation, tied by value
         against its own system rows).  MD-super HOLDS.

  M-RANK (rank pricing): ATOMS = arbitrary rank-one matrices |u><v|.
         Closed form: c_rank(x) = eps * rank(x).  Lower bound: rank is
         subadditive over rank-<=1 atoms (cited standard + computed
         spot-check, not proved in-module); attainment: an exact rank-one factorization is
         constructed for every sampled x and its atom count equals the
         rank, computed by Gaussian elimination over Q and re-computed
         by a second, separately written largest-nonvanishing-minor
         path (independent as written; an extensionally equal
         implementation is indistinguishable, the same genre as the
         eps NOTE below).  On
         x = E_01 +- E_02 = |0>(<1| +- <2|): rank 1, c_rank = eps
         < 2*eps.  MD-super FAILS.

THE P-BATTERY.  The property list P (spec Sec. 2, quoted set-exactly
as module data P_FROZEN; the freeze's provenance lives in the
build-spec and charter artifacts, not in this file) is evaluated as
executable predicates
against BOTH models: P-1 argmin diagonal (tied by value to the word
module's A2-argmin at the uniform floor), P-2 unit pricing (tied to
psi_min on the complete uniform carrier, open-word argmin), P-3 disjoint
additivity (spot-check form), P-4 eps-linearity (two ratios), P-5
faithfulness + floor, P-6 set pricing untouched (def:aps keeps the
counting measure; the models price presentations), P-7 no conflict with
the trio's computed banked legs (the claims-reviewed table is module
data, set-exact against the three siblings' own check inventories, with
a category and a reason per check).  Every P-1..P-6 cell of the model
x property table is COMPUTED, with P-6 model-independent by
construction; the P-7 cell computes names set-exactness, nonlinearity
witnesses, and unit agreement, while part of its claims-reviewed table
is per-row classification, labelled as such row by row.  Each of
P-1..P-5 carries a boundary phrase asserted verbatim, with witness
pricers at the stated boundary passing the matching _p* predicate,
out-of-boundary witness pricers failing it, and a linear witness
pricer failing _p7's nonlinearity clause.  Both models satisfy all
of P.

FUNCTIONAL LINEARITY IS NOT IN P (spec Sec. 2, verified by the
2026-08-04 audit-first walk): it is consumed in the trio under
LINEAR_REALIZATION_TARGET (elliptope E1) and stipulated at two P40
sites, never derived.  Both models are exhibited NON-LINEAR (witnesses
computed for each), which is how they live outside the elliptope
parametrization without contradicting any of its computed legs.

THE SEPARATION.  Over the SAME quantifier domain -- all signed
2-element separator sets, all four sign patterns, at n = 3 and 4
(60 and 264 instances, the same totals as the md_super sibling's N1
system, whose (S, signs) enumeration this module's domain equals
set-exactly) -- MD-super's weak-form inequality c(x) >= 2*eps is TRUE
in M-ENV at every instance with EQUALITY (zero slack), and FALSE in
M-RANK at exactly the rank-deficient instances: 24 of 60 at n = 3,
96 of 264 at n = 4, each priced at exactly eps.

THE INDEPENDENCE CONCLUSION, stated FROM P AS FROZEN, both directions,
as a computed record: MD_SUPER_NODISCOUNT is NOT ENTAILED by P (M-RANK
satisfies every property in P and violates the premise -- witnessed,
counted) and NOT REFUTED by P (M-ENV satisfies every property in P and
satisfies the premise -- witnessed, zero violations).  Scope, carried
in the record and NOT smoothed over: complete uniform carrier only;
signed unit coefficients {+1,-1,0} only.  The rank model is a model of
P, not of the world.

ATOM-ADMISSIBILITY INCLUSION.  Every envelope atom is rank one
(computed), so the envelope atom set is INCLUDED in the rank atom set,
and pointwise c_rank(x) <= c_env(x) on every sampled x (computed, with
strict sites counted).  The divergence sites on the 2-set domain are
EXACTLY the rank-deficient signed combinations (equivalently: the two
separators share a source vertex OR share a target vertex; both
characterizations computed and compared as sets).  The md_super
sibling's N1 BINDING sets (its source-sharing sets, re-read here from
its own nodiscount_system rows) are a strict subset of the divergence
sites: 12 of 24 signed instances at n = 3, 48 of 96 at n = 4 -- the
binding sets are the divergence sites that carry off-diagonal content
in the LINEAR family; target-sharing sets also diverge but contribute
only constant forms there.  (The spec's Sec. 5 gloss "the divergence
sites are exactly the source-sharing (rank-deficient) signed sets" is
computed here in its exact form: divergence = rank-deficiency =
source-sharing UNION target-sharing; the source-sharing part is exactly
N1's binding set.  Recorded as a build-seat judgment call in
BUILD_RETURN.md.)

THE LOAD-SEMANTICS BRIDGE, computed and NOT decided: the premise is
written phi(x^T x) >= k*eps; the models price x directly.
rank(x^T x) = rank(x) is computed on every sampled x (6155 instances).
Clause (i) of the residual (load semantics) is exactly what identifies
c(x) with phi(x^T x); the models take positions on c, and that
identification is part of what the premise asserts.  The models do NOT
decide clause (i).

THE SCOPE FENCE, computed as the REASON it is drawn: off the complete
uniform carrier BOTH models diverge from the banked psi_min -- on the
path P3, psi_min(E_02) = 2*eps by word distance while
c_env(E_02) = c_rank(E_02) = eps.  On the complete uniform carrier both
models agree with psi_min on every matrix unit (control).  The
independence claim is scoped to the complete uniform carrier -- the
same arena as the trio's own center-selection conclusion, so the
scoping does not weaken the result relative to the charter.

READING, in this docstring and in NO leg and NO returned field (flagged
for the auditor exactly as the trio flags its readings): the exact
content this module exhibits for the premise MD_SUPER_NODISCOUNT is the
ATOM-ADMISSIBILITY CHOICE -- which decomposition atoms the enforcement
ledger admits when pricing a superposition.  Admit only the word-image
atoms and costs cannot cancel (M-ENV, the premise holds tight); admit
every rank-one atom and a source-sharing superposition collapses to a
single atom (M-RANK, the premise fails).  That choice is the residual's
clause (ii) -- whether MD's "costs do not cancel" governs objects the
combinatorial carrier cannot write -- one level down: not whether the
clause applies, but which decompositions it quantifies over.  On that
reading the premise is a physical commitment about the ledger's atom
set, and this module computes that P as frozen does not make it.

eps NOTE (the siblings' note, carried): eps enters only through the
word module's probed_eps() singleton probe on the banked
``symmetry_cost_floor.config_cost``.  An extensionally correct bypass
of the probe is invisible BY EXTENSIONALITY; at the unit probe eps = 1,
so a value-equal literal substituted for eps is likewise invisible.
The scaled re-runs (factors 2 and 3) are leg content: each consuming
leg asserts the scales are distinct from the base and from each other.

------------------------------------------------------------------------------
PREMISES, SET-EXACT (carried as data below; declarations, audited from
outside, not self-enforced)
------------------------------------------------------------------------------
CONSUMED (exactly the word module's inventory, imported and compared
set-exactly): LINEAR_REALIZATION_TARGET (separators realize as matrix
units; the models price the realized algebra elements); A2_ARGMIN (the
argmin diagonal both models are tied to); FD3_FLOOR (probed);
FD4_FINITE_CARRIER; DEF_APS_STRUCTURE_COST (P-6);
EQUAL_COST_UNIFORMITY; CARRIER_COMPLETENESS (the scope fence);
NONEMPTY_ENFORCEMENT_PRESENTATION.
NOT CONSUMED: MD_SUPER_NODISCOUNT -- the OBJECT OF STUDY, not a
premise; this module evaluates it in two models and consumes it
nowhere, so every returned record carries conditional_on: [] (empty).
Also not consumed: FUNCTIONAL_LINEARITY (the point: it is NOT in P);
REAL_SYMMETRIC_TEST_SECTOR; P1_SANDWICH_REALIZATION;
P2_PRESENTATION_GAUGE; P3_UNDERIVED; CYCLICITY;
PHI_EQ_EPS_TR_STIPULATION; DET_MAX_SELECTION_PRINCIPLE;
MISSING_LEMMA_EQUALITY_AS_PREMISE.

MAY NOT CITE (spec Sec. 6, inheriting the charter's):
- "Born is derived."  "MD implies Born."  "The carrier gap is closed."
  "The residual is discharged."
- "MD-super is FALSE."  The rank model is a model of P, not of the
  world; the result is independence FROM P, scoped as above.
- "Clause (i) is decided."  The bridge rank(x^T x) = rank(x) is
  computed; the identification of c(x) with phi(x^T x) is part of what
  the premise asserts and is not decided here.
- Any sentence attributing content here to what the module PREVENTS.
  It computes; it does not prevent.
"""

import hashlib

from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from collections import Counter

from apf.word_carrier_transfer import (
    probed_eps, argmin_values, uniform_cost, unit_matrix, matmul, all_pairs,
    EXPECTED_LEGS as WORD_EXPECTED_LEGS,
    PREMISES_CONSUMED as WORD_PREMISES_CONSUMED,
    _fixtures as _referee_fixtures,
    _run_predicates as _referee_predicates,
)
from apf.carrier_elliptope import (
    mt, matrix_rank, det_exact,
    EXPECTED_LEGS as ELL_EXPECTED_LEGS,
)
from apf.md_super_nodiscount import (
    separators, signed_combo, nodiscount_system,
    EXPECTED_LEGS as MD_EXPECTED_LEGS,
    PREMISES_CONSUMED as MD_PREMISES_CONSUMED,
    RESIDUAL_PREMISES as MD_RESIDUAL_PREMISES,
    check_L_premise_inventory_set_exact as _md_premise_check,
)

# ---------------------------------------------------------------------------
# premises and frozen-P data
# ---------------------------------------------------------------------------

PREMISES_CONSUMED = frozenset(WORD_PREMISES_CONSUMED)
OBJECT_OF_STUDY = frozenset({"MD_SUPER_NODISCOUNT"})
PREMISES_NOT_CONSUMED = frozenset({
    "MD_SUPER_NODISCOUNT", "FUNCTIONAL_LINEARITY",
    "REAL_SYMMETRIC_TEST_SECTOR", "P1_SANDWICH_REALIZATION",
    "P2_PRESENTATION_GAUGE", "P3_UNDERIVED", "CYCLICITY",
    "PHI_EQ_EPS_TR_STIPULATION", "DET_MAX_SELECTION_PRINCIPLE",
    "MISSING_LEMMA_EQUALITY_AS_PREMISE",
})
CONDITIONAL_ON = []   # the independence facts are unconditional [P_math]
                      # statements about two constructed models

# The property list P, quoted set-exactly from the build spec Sec. 2.
# A candidate cost functional c on presentations x (real
# matrices over the complete uniform carrier K_n, signed unit
# coefficients) must satisfy, set-exactly:
P_FROZEN = {
    "P-1": "argmin diagonal: c(E_ii) = eps for every diagonal unit (the "
           "word module's A2-argmin at the uniform floor).",
    "P-2": "unit pricing: c(E_ij) = eps for every matrix unit, matching "
           "psi_min on the complete uniform carrier.",
    "P-3": "disjoint additivity: c(x + y) = c(x) + c(y) when x, y have "
           "vertex-disjoint supports (def:aps-shaped additivity over "
           "disjoint structures; spot-check form as in the word module's "
           "referee predicate (a)).",
    "P-4": "eps-linearity: c scales linearly in the unit eps (two "
           "ratios, per the R0 probe convention).",
    "P-5": "faithfulness + floor: c(x) = 0 iff x = 0; c(x) >= eps for "
           "x != 0 (FD3's positive floor).",
    "P-6": "set pricing untouched: def:aps structure cost C(E) = sum "
           "c(d) on SETS of separators is not modified; the candidate "
           "prices presentations (algebra elements), sets keep the "
           "counting measure.",
    "P-7": "no conflict with banked legs: the candidate contradicts no "
           "COMPUTED banked leg of the v24.3.465 trio.  The elliptope "
           "statements (E1-E5) are theorems about LINEAR functionals "
           "and are conditioned as such; the md_super statements are "
           "conditional_on the premise.",
}
# The seven property TEXTS pinned by sha256 over the canonical
# serialization (sorted keys, "key: text", newline-joined); compared
# in the p_frozen leg (second-audit MINOR-1).  The sha is minted in
# this module over the dict above: a drift marker for the text as
# written here, not a certificate of fidelity to the external spec or
# of when the text was frozen (third-audit MAJOR-2).  The text <->
# executable correspondence is exercised by value in the
# p_texts_tied_to_executables_boundary leg.
P_FROZEN_SHA256 = (
    "85bfd9e2fa5316a616d67917270caa8bfd6e07ab7b920e34c951dbadc21707c5")

NOT_IN_P = frozenset({"FUNCTIONAL_LINEARITY"})

MODELS = {
    "M_ENV": {
        "atoms": "matrix units E_ij (the word image)",
        "closed_form": "c_env(x) = eps * |supp(x)|",
        "md_super_verdict": "HOLDS (tight: equality at every instance)",
    },
    "M_RANK": {
        "atoms": "arbitrary rank-one matrices |u><v|",
        "closed_form": "c_rank(x) = eps * rank(x)",
        "md_super_verdict": "FAILS (at exactly the rank-deficient "
                            "signed sets)",
    },
}

SCOPE = {
    "carrier": "complete uniform carrier only (off it both models "
               "diverge from banked psi_min; computed, the P3 leg)",
    "coefficients": "signed unit coefficients {+1,-1,0} only "
                    "(coefficient-magnitude semantics are undetermined "
                    "by the frozen surface)",
    "bridge": "rank(x^T x) = rank(x) computed on every sampled x; "
              "clause (i) load semantics is what identifies c(x) with "
              "phi(x^T x) and is not decided here",
}

CONCLUSION = {
    "not_entailed_by_P": True,
    "witness_not_entailed": "M_RANK",
    "not_refuted_by_P": True,
    "witness_not_refuted": "M_ENV",
    "scope": SCOPE,
}

# P-7: the trio's checks, each with (category, why-untouched).  Keys are
# compared set-exactly against the three siblings' own EXPECTED_LEGS
# inventories.  Categories: word-sector (statements about words / the
# carrier graph / declared candidate records, which the models do not
# touch), linear-family-conditioned (quantifies over LINEAR functionals;
# both models are computed non-linear, outside that family),
# conditional_on_premise (the md_super records carry
# conditional_on [MD_SUPER_NODISCOUNT]; they compute consequences of the
# premise inside the linear family, which neither model contradicts as
# arithmetic).
BANKED_CLAIMS_REVIEWED = {
    "check_L_banked_cost_probe": (
        "word-sector",
        "probe semantics on the banked cost; both models read eps "
        "through the same probe and change nothing about it "
        "(classification, not computed in-module)"),
    "check_L_word_fiber_obstruction": (
        "word-sector",
        "a statement about contraction fibers of words on the carrier "
        "graph; the models price algebra elements, not words "
        "(classification, not computed in-module)"),
    "check_T_argmin_transfer_diagonal": (
        "word-sector",
        "psi_min diagonal closed forms; both models agree with the "
        "computed values on the complete uniform carrier (the P-1 tie)"),
    "check_T_block_constant_from_global_floor": (
        "word-sector",
        "per-vertex prices on disconnected carriers, off the complete "
        "uniform carrier and outside this module's fence "
        "(classification, not computed in-module)"),
    "check_L_full_extension_not_forced": (
        "linear-family-conditioned",
        "its two-model witness quantifies within LINEAR extensions of "
        "psi_min; both models here are non-linear (witnessed) and "
        "outside that family"),
    "check_T_carrier_transfer_referee": (
        "word-sector",
        "a verdict table over declared candidate records; neither "
        "model is one of its fixtures (computed in-leg: "
        "referee_predicates_run_on_model_records)"),
    "check_T_carrier_consistent_functionals_are_elliptope": (
        "linear-family-conditioned",
        "E1 parametrizes LINEAR functionals with the carrier diagonal; "
        "both models are non-linear (witnessed), outside the family"),
    "check_T_two_models_center_and_extreme": (
        "linear-family-conditioned",
        "both of its models are points W of the linear family; "
        "this module's models are not"),
    "check_L_missing_lemma_is_center_selection": (
        "linear-family-conditioned",
        "the constraint system ranges over linear W-functionals; its "
        "computed rows are re-read here as objects, not contradicted"),
    "check_T_trace_is_determinant_maximal": (
        "linear-family-conditioned",
        "det W over the elliptope of linear functionals; the models "
        "have no W"),
    "check_L_word_route_strengthenings": (
        "linear-family-conditioned",
        "the E5(ii) distance law is about the LINEAR open-word "
        "extension psi; the E5(i) kernel rule is word-sector graph "
        "theory; either category leaves it untouched by the models; "
        "off-complete-carrier scope is fenced here"),
    "check_T_nodiscount_center_selection": (
        "conditional_on_premise",
        "conditional_on [MD_SUPER_NODISCOUNT]; its system rows are "
        "re-read here by value (the zero-slack tie), not contradicted"),
    "check_L_recovered_k_resolution_equality": (
        "conditional_on_premise",
        "conditional_on the premise; equality at the center of the "
        "linear family, which neither model inhabits"),
    "check_T_chain_closure_sandwich_symmetry": (
        "conditional_on_premise",
        "conditional_on the premise; sandwich-sector closure inside "
        "the linear family"),
    "check_L_premise_inventory_set_exact": (
        "conditional_on_premise",
        "a data check on the sibling's own premise sets; untouched"),
}

# ---------------------------------------------------------------------------
# exact helpers
# ---------------------------------------------------------------------------

def zmat(n):
    return [[F(0)] * n for _ in range(n)]

def cellmat(n, entries):
    x = zmat(n)
    for (i, j, s) in entries:
        x[i][j] = F(s)
    return x

def madd(a, b, n):
    return [[a[i][j] + b[i][j] for j in range(n)] for i in range(n)]

def supp_size(x):
    return sum(1 for row in x for v in row if v != 0)

def vertex_set(x, n):
    vs = set()
    for i in range(n):
        for j in range(n):
            if x[i][j] != 0:
                vs.add(i)
                vs.add(j)
    return vs

def signed_presentations(n, max_supp):
    """All matrices over K_n cells with entries in {+1,-1} on a support
    of size 1..max_supp (the signed unit-coefficient domain)."""
    cells = [(i, j) for i in range(n) for j in range(n)]
    out = []
    for s in range(1, max_supp + 1):
        for cc in combinations(cells, s):
            for signs in product((1, -1), repeat=s):
                x = zmat(n)
                for (i, j), e in zip(cc, signs):
                    x[i][j] = F(e)
                out.append(x)
    return out

def rank_by_minors(M):
    """INDEPENDENT rank path: the largest r such that some r x r minor
    is nonzero (exact, over Q)."""
    n = len(M)
    best = 0
    for r in range(1, n + 1):
        found = False
        for rows in combinations(range(n), r):
            for cols in combinations(range(n), r):
                sub = [[M[i][j] for j in cols] for i in rows]
                if det_exact(sub) != 0:
                    found = True
                    break
            if found:
                break
        if not found:
            break
        best = r
    return best

def rank_one_factorization(x, n):
    """An exact rank-one decomposition x = sum of rank-<=1 atoms
    (coefficient +1 each; the sign is absorbed into the atom, which the
    rank atom set admits).  Standard pivot elimination: each step zeroes
    the pivot row and column, so it terminates in rank(x) steps."""
    r = [row[:] for row in x]
    atoms = []
    while True:
        assert len(atoms) <= n * n, (
            "rank_one_factorization: step bound n*n exceeded")
        piv = next(((i, j) for i in range(n) for j in range(n)
                    if r[i][j] != 0), None)
        if piv is None:
            break
        i0, j0 = piv
        col = [r[i][j0] for i in range(n)]
        row = [r[i0][j] / r[i0][j0] for j in range(n)]
        atom = [[col[i] * row[j] for j in range(n)] for i in range(n)]
        atoms.append(atom)
        r = [[r[i][j] - atom[i][j] for j in range(n)] for i in range(n)]
    return atoms

def env_atoms(n):
    """The M-ENV atom set with signs applied: {+E_ij, -E_ij}."""
    atoms = []
    for i in range(n):
        for j in range(n):
            for s in (1, -1):
                u = unit_matrix(n, i, j)
                atoms.append([[F(s) * u[r][c] for c in range(n)]
                              for r in range(n)])
    return atoms

def env_cell_witness(x, n):
    """The attaining witness for M-ENV: one signed unit atom per
    nonzero cell.  Returns [(coefficient, unit_atom)] with coefficients
    in {+1,-1} on the signed domain."""
    w = []
    for i in range(n):
        for j in range(n):
            if x[i][j] != 0:
                u = unit_matrix(n, i, j)
                w.append((x[i][j], u))
    return w

def env_brute_min(x, n, kmax):
    """The M-ENV argmin by exhaustive enumeration over multisets of
    signed unit atoms of size <= kmax.  Returns the minimal k, or None
    if no decomposition of size <= kmax exists."""
    if all(v == 0 for row in x for v in row):
        return 0
    atoms = env_atoms(n)
    for k in range(1, kmax + 1):
        for combo in combinations_with_replacement(range(len(atoms)), k):
            acc = zmat(n)
            for t in combo:
                acc = madd(acc, atoms[t], n)
            if acc == x:
                return k
    return None

# ---------------------------------------------------------------------------
# the two models (closed-form evaluators; certified by the two
# closed-form checks below via witness + independent-path legs)
# ---------------------------------------------------------------------------

def env_price(x, n, e):
    """M-ENV on the signed domain: eps * |supp(x)|."""
    return e * supp_size(x)

def rank_price(x, n, e):
    """M-RANK: eps * rank(x)."""
    return e * matrix_rank(x)

def two_set_domain(n):
    """The MD-super weak-form quantifier domain: all signed 2-element
    separator sets, all four sign patterns."""
    seps = separators(n)
    dom = []
    for S in combinations(seps, 2):
        for signs in product((1, -1), repeat=2):
            dom.append((S, signs, signed_combo(n, S, signs)))
    return dom

# larger sampled cases: (n, entries, expected_supp, expected_rank)
LARGER_SAMPLES = [
    (5, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)], 4, 4),
    (5, [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1)], 4, 1),
    (5, [(0, 1, 1), (0, 2, -1), (2, 1, 1), (2, 2, -1)], 4, 1),
    (4, [(0, 0, 1), (1, 1, 1), (2, 2, 1), (3, 3, 1)], 4, 4),
    (4, [(0, 1, 1), (1, 0, 1), (2, 3, 1), (3, 2, 1)], 4, 4),
]

# ---------------------------------------------------------------------------
# the P predicates (shared by the P-battery check and the conclusion
# record's model x property table, so the table is computed, not copied)
# ---------------------------------------------------------------------------

def _p1(pricefn, e0):
    ok = True
    for n in (3, 4):
        vals, _ = argmin_values(uniform_cost(n, e0), 6, "set",
                                closed_only=True)
        ok = ok and all(
            vals[(i, i)] == e0
            and pricefn(unit_matrix(n, i, i), n, e0) == vals[(i, i)]
            for i in range(n))
    return ok

def _p2(pricefn, e0):
    ok = True
    for n in (3, 4):
        vals, _ = argmin_values(uniform_cost(n, e0), 6, "set",
                                closed_only=False)
        ok = ok and all(
            vals[(i, j)] == e0
            and pricefn(unit_matrix(n, i, j), n, e0) == vals[(i, j)]
            for i in range(n) for j in range(n))
    return ok

def _p3(pricefn, e0):
    samples = [
        (4, [(0, 1, 1)], [(2, 3, 1)]),
        (4, [(0, 1, -1)], [(2, 3, 1)]),
        (4, [(0, 1, 1), (1, 0, 1)], [(2, 3, 1), (3, 2, -1)]),
        (4, [(0, 1, 1), (1, 0, -1)], [(2, 3, 1), (3, 2, 1)]),
        (5, [(0, 1, 1), (1, 2, 1)], [(3, 4, -1)]),
    ]
    ok = len(samples) == 5
    for n, ex, ey in samples:
        x, y = cellmat(n, ex), cellmat(n, ey)
        ok = (ok and (vertex_set(x, n) & vertex_set(y, n) == set())
              and pricefn(madd(x, y, n), n, e0)
                  == pricefn(x, n, e0) + pricefn(y, n, e0))
    return ok

def _p4(pricefn, e0):
    xs = signed_presentations(3, 3)[::97]
    base = [pricefn(x, 3, e0) for x in xs]
    ok = len(xs) > 0 and all(v > 0 for v in base)
    for s in (2, 3):
        se = s * e0
        ok = (ok and se != e0
              and [pricefn(x, 3, se) for x in xs]
                  == [s * v for v in base])
    return ok

def _p5(pricefn, e0):
    dom = signed_presentations(3, 3)
    z = zmat(3)
    return (pricefn(z, 3, e0) == 0
            and len(dom) == 834
            and all(pricefn(x, 3, e0) >= e0 for x in dom)
            and all(pricefn(x, 3, e0) != 0 for x in dom))

def _p6(e0):
    """Model-independent by construction: neither model defines a set
    price; def:aps keeps the counting measure."""
    uc = uniform_cost(4, e0)
    sets = [[(0, 1)], [(0, 1), (2, 3)], [(0, 1), (1, 2), (2, 3)]]
    ok = all(
        sum(uc[frozenset(p)] for p in S) == e0 * len(S) for S in sets)
    # the contrast that P-6 protects: the SET {s01, s02} keeps price
    # 2*eps while the rank model prices its superposition at eps
    x = cellmat(3, [(0, 1, 1), (0, 2, 1)])
    set_price = uc[frozenset((0, 1))] + uc[frozenset((0, 2))]
    return (ok and set_price == 2 * e0
            and rank_price(x, 3, e0) == e0
            and env_price(x, 3, e0) == set_price)

def _p7(pricefn, e0):
    trio_names = sorted(list(WORD_EXPECTED_LEGS) + list(ELL_EXPECTED_LEGS)
                        + list(MD_EXPECTED_LEGS))
    names_ok = sorted(BANKED_CLAIMS_REVIEWED) == trio_names
    x1, y1 = cellmat(3, [(0, 1, 1)]), cellmat(3, [(0, 1, -1)])
    x2, y2 = cellmat(3, [(0, 1, 1)]), cellmat(3, [(0, 2, 1)])
    nonlinear = any(
        pricefn(madd(x, y, 3), 3, e0) != pricefn(x, 3, e0)
        + pricefn(y, 3, e0)
        for x, y in ((x1, y1), (x2, y2)))
    vals, _ = argmin_values(uniform_cost(3, e0), 6, "set",
                            closed_only=False)
    agree = all(pricefn(unit_matrix(3, i, j), 3, e0) == vals[(i, j)]
                for i in range(3) for j in range(3))
    return names_ok and nonlinear and agree

def _p_cell(model_name, pid, e0):
    fn = env_price if model_name == "M_ENV" else rank_price
    if pid == "P-1":
        return _p1(fn, e0)
    if pid == "P-2":
        return _p2(fn, e0)
    if pid == "P-3":
        return _p3(fn, e0)
    if pid == "P-4":
        return _p4(fn, e0)
    if pid == "P-5":
        return _p5(fn, e0)
    if pid == "P-6":
        return _p6(e0)
    if pid == "P-7":
        return _p7(fn, e0)
    raise ValueError(pid)

# ---------------------------------------------------------------------------
# result plumbing: set-exact leg inventory enforced on the check path
# ---------------------------------------------------------------------------

EXPECTED_LEGS = {
    "check_T_env_closed_form_support_pricing": [
        "atoms_have_support_one_signed",
        "brute_force_argmin_matches_exhaustive_n3",
        "lower_bound_support_subadditive_sampled",
        "sampled_larger_cases_supp_up_to_five",
        "scaled_eps_two_ratios_tied",
        "witness_attains_support_count_exhaustive_n3_n4",
    ],
    "check_T_rank_closed_form_rank_pricing": [
        "factorization_witness_attains_rank_exhaustive_n3_n4",
        "independent_rank_by_minors_agrees",
        "rank_subadditivity_spot_checked_with_strict",
        "sampled_larger_cases_rank_up_to_four",
        "scaled_eps_two_ratios_tied",
    ],
    "check_T_p_battery_both_models": [
        "p1_argmin_diagonal_both_models",
        "p2_unit_pricing_matches_psi_min",
        "p3_disjoint_additivity_spot_both_models",
        "p4_eps_linearity_two_ratios_both_models",
        "p5_faithfulness_and_floor_both_models",
        "p6_set_pricing_counting_measure_kept",
        "p_texts_tied_to_executables_boundary",
    ],
    "check_L_p7_banked_trio_claims_untouched": [
        "md_residual_data_tied",
        "models_nonlinear_outside_linear_family",
        "reason_categories_valid_and_counts",
        "referee_predicates_run_on_model_records",
        "trio_check_names_set_exact",
        "word_sector_unit_agreement_complete_uniform",
    ],
    "check_T_separation_and_two_verdicts": [
        "domain_counts_and_sign_tuples_complete",
        "e01_pm_e02_both_signs_values",
        "env_center_price_tie_to_n1_rows",
        "md_super_false_in_rank_with_counts",
        "md_super_true_in_env_zero_slack",
        "model_verdict_strings_tied_to_counts",
        "source_sharing_family_per_instance",
    ],
    "check_L_atom_admissibility_and_bridge": [
        "bridge_rank_xtx_equals_rank_x",
        "divergence_exactly_rank_deficient",
        "env_atoms_are_rank_one_inclusion",
        "n1_binding_sets_source_sharing_divergent_subset",
        "pointwise_dominance_with_strict_sites",
    ],
    "check_T_independence_conclusion_record": [
        "model_property_table_all_cells_computed",
        "not_entailed_witnessed_by_rank_model",
        "not_refuted_witnessed_by_env_model",
        "p_frozen_set_exact_and_not_in_p",
        "premise_inventory_set_exact",
        "scope_fields_computed",
    ],
    "check_L_scope_fence_and_nonlinearity": [
        "complete_carrier_agreement_control",
        "nonlinearity_witness_env",
        "nonlinearity_witness_rank",
        "p3_carrier_divergence_reason",
        "signed_domain_verified",
    ],
}

def _result(name, legs, fails, key_result):
    exp = EXPECTED_LEGS[name]
    got = sorted(legs)
    if got != exp:
        raise AssertionError(
            f"{name}: leg inventory mismatch: {got} != {exp}")
    for k, v in legs.items():
        if v is not True:
            fails.append(f"leg not True: {k}")
    return {
        "name": name,
        # passed reads the legs directly in addition to the fails
        # funnel (third-audit M20)
        "passed": not fails and all(v is True for v in legs.values()),
        "legs": dict(legs),
        "fails": list(fails),
        "key_result": key_result,
        "conditional_on": list(CONDITIONAL_ON),
        "tier": 3,
        "epistemic": "P_math",
        "status": "banked v24.3.466 (2026-08-04)",
    }

# ---------------------------------------------------------------------------
# closed forms
# ---------------------------------------------------------------------------

def check_T_env_closed_form_support_pricing():
    legs, fails = {}, []
    e0 = probed_eps()[0]
    # atoms: every M-ENV atom has support exactly one, entries +-1
    atom_counts, atom_ok = [], []
    for n in (3, 4):
        ats = env_atoms(n)
        atom_counts.append(len(ats))
        atom_ok.append(all(
            supp_size(a) == 1
            and all(v in (F(1), F(-1), F(0)) for row in a for v in row)
            for a in ats))
    legs["atoms_have_support_one_signed"] = (
        atom_ok == [True, True] and atom_counts == [18, 32])
    # attaining witness, exhaustive n = 3, 4 with support <= 3
    counts, wit_ok = [], []
    for n in (3, 4):
        dom = signed_presentations(n, 3)
        counts.append(len(dom))
        flag = len(dom) > 0
        for x in dom:
            w = env_cell_witness(x, n)
            s = zmat(n)
            for coef, u in w:
                s = madd(s, [[coef * u[r][c] for c in range(n)]
                             for r in range(n)], n)
            flag = (flag and s == x
                    and len(w) == supp_size(x)
                    and all(coef in (F(1), F(-1)) for coef, _ in w)
                    and all(supp_size(u) == 1 for _, u in w)
                    and env_price(x, n, e0) == e0 * len(w))
        wit_ok.append(flag)
    legs["witness_attains_support_count_exhaustive_n3_n4"] = (
        wit_ok == [True, True] and counts == [834, 4992])
    # brute-force argmin, exhaustive at n = 3 support <= 2, plus 12
    # stride-sampled support-3 presentations with full k <= 3 search
    dom_small = signed_presentations(3, 2)
    brute_ok = (len(dom_small) == 162 and all(
        env_brute_min(x, 3, supp_size(x)) == supp_size(x)
        and env_price(x, 3, e0) == e0 * env_brute_min(x, 3, supp_size(x))
        for x in dom_small))
    dom3_supp3 = [x for x in signed_presentations(3, 3)
                  if supp_size(x) == 3]
    samples3 = dom3_supp3[::56]
    brute3_ok = (len(dom3_supp3) == 672 and len(samples3) == 12 and all(
        env_brute_min(x, 3, 3) == 3
        and env_price(x, 3, e0) == 3 * e0 for x in samples3))
    legs["brute_force_argmin_matches_exhaustive_n3"] = (
        brute_ok and brute3_ok)
    # lower bound: |supp(sum of k support-one atoms)| <= k, sampled
    # multisets including strict (cancelling / repeated) instances
    ats3 = env_atoms(3)
    multisets = [[0], [0, 0], [0, 1], [0, 2, 1], [2, 4, 6],
                 [0, 2, 4, 6], [3, 3, 2]]
    lb_pairs = []
    for ms in multisets:
        acc = zmat(3)
        for t in ms:
            acc = madd(acc, ats3[t], 3)
        lb_pairs.append((supp_size(acc), len(ms)))
    legs["lower_bound_support_subadditive_sampled"] = (
        len(lb_pairs) == 7
        and all(s <= k for s, k in lb_pairs)
        and any(s < k for s, k in lb_pairs))
    # sampled larger cases (n = 4, 5; support 4)
    lg_ok = len(LARGER_SAMPLES) == 5
    for n, entries, es, er in LARGER_SAMPLES:
        x = cellmat(n, entries)
        w = env_cell_witness(x, n)
        lg_ok = (lg_ok and supp_size(x) == es and len(w) == es
                 and env_price(x, n, e0) == e0 * es)
    legs["sampled_larger_cases_supp_up_to_five"] = lg_ok
    # scaled eps, two ratios, tied by value
    dom3 = signed_presentations(3, 3)
    base = [env_price(x, 3, e0) for x in dom3]
    sc_ok = len(base) == 834
    scales_used = []
    for s in (2, 3):
        se = s * e0
        scales_used.append(se)
        sc_ok = (sc_ok and se != e0
                 and [env_price(x, 3, se) for x in dom3]
                     == [s * v for v in base])
    legs["scaled_eps_two_ratios_tied"] = (
        sc_ok and len(set(scales_used)) == 2)
    return _result("check_T_env_closed_form_support_pricing", legs, fails,
                   {"exhaustive_counts": counts,
                    "brute_force_small_domain": len(dom_small),
                    "brute_force_supp3_samples": len(samples3),
                    "atom_counts": atom_counts})

def check_T_rank_closed_form_rank_pricing():
    legs, fails = {}, []
    e0 = probed_eps()[0]
    counts, fac_ok = [], []
    minor_checked, minor_ok = 0, True
    for n in (3, 4):
        dom = signed_presentations(n, 3)
        counts.append(len(dom))
        flag = len(dom) > 0
        stride = 1 if n == 3 else 9
        for idx, x in enumerate(dom):
            r1 = matrix_rank(x)
            atoms = rank_one_factorization(x, n)
            s = zmat(n)
            for a in atoms:
                s = madd(s, a, n)
            flag = (flag and s == x
                    and len(atoms) == r1
                    and all(matrix_rank(a) <= 1 for a in atoms)
                    and rank_price(x, n, e0) == e0 * r1
                    and rank_price(x, n, e0) == e0 * len(atoms))
            if idx % stride == 0:
                minor_checked += 1
                minor_ok = minor_ok and rank_by_minors(x) == r1
        fac_ok.append(flag)
    legs["factorization_witness_attains_rank_exhaustive_n3_n4"] = (
        fac_ok == [True, True] and counts == [834, 4992])
    lg_minor = all(rank_by_minors(cellmat(n, entries))
                   == matrix_rank(cellmat(n, entries))
                   for n, entries, _, _ in LARGER_SAMPLES)
    legs["independent_rank_by_minors_agrees"] = (
        minor_ok and minor_checked == 834 + 555 and lg_minor)
    # rank subadditivity, spot-checked with strict instances (cited
    # standard; not proved in-module)
    base = signed_presentations(3, 2)
    pairs = [(base[i], base[-1 - i]) for i in range(0, len(base), 5)]
    sub_trips = [(matrix_rank(madd(a, b, 3)), matrix_rank(a),
                  matrix_rank(b)) for a, b in pairs]
    legs["rank_subadditivity_spot_checked_with_strict"] = (
        len(sub_trips) == 33
        and all(rab <= ra + rb for rab, ra, rb in sub_trips)
        and any(rab < ra + rb for rab, ra, rb in sub_trips))
    lg_ok = len(LARGER_SAMPLES) == 5
    ranks_seen = set()
    for n, entries, es, er in LARGER_SAMPLES:
        x = cellmat(n, entries)
        atoms = rank_one_factorization(x, n)
        s = zmat(n)
        for a in atoms:
            s = madd(s, a, n)
        lg_ok = (lg_ok and matrix_rank(x) == er and len(atoms) == er
                 and s == x and rank_price(x, n, e0) == e0 * er)
        ranks_seen.add(er)
    legs["sampled_larger_cases_rank_up_to_four"] = (
        lg_ok and 4 in ranks_seen and 1 in ranks_seen)
    dom3 = signed_presentations(3, 3)
    base_v = [rank_price(x, 3, e0) for x in dom3]
    sc_ok = len(base_v) == 834
    scales_used = []
    for s in (2, 3):
        se = s * e0
        scales_used.append(se)
        sc_ok = (sc_ok and se != e0
                 and [rank_price(x, 3, se) for x in dom3]
                     == [s * v for v in base_v])
    legs["scaled_eps_two_ratios_tied"] = (
        sc_ok and len(set(scales_used)) == 2)
    return _result("check_T_rank_closed_form_rank_pricing", legs, fails,
                   {"exhaustive_counts": counts,
                    "independent_rank_path_checked": minor_checked,
                    "subadditivity_pairs": len(sub_trips)})

# ---------------------------------------------------------------------------
# the P-battery
# ---------------------------------------------------------------------------

def check_T_p_battery_both_models():
    legs, fails = {}, []
    e0 = probed_eps()[0]
    legs["p1_argmin_diagonal_both_models"] = (
        _p1(env_price, e0) is True and _p1(rank_price, e0) is True
        and env_price(unit_matrix(3, 0, 0), 3, e0) == e0
        and rank_price(unit_matrix(3, 0, 0), 3, e0) == e0)
    legs["p2_unit_pricing_matches_psi_min"] = (
        _p2(env_price, e0) is True and _p2(rank_price, e0) is True
        and env_price(unit_matrix(3, 0, 2), 3, e0) == e0
        and rank_price(unit_matrix(3, 0, 2), 3, e0) == e0)
    legs["p3_disjoint_additivity_spot_both_models"] = (
        _p3(env_price, e0) is True and _p3(rank_price, e0) is True)
    legs["p4_eps_linearity_two_ratios_both_models"] = (
        _p4(env_price, e0) is True and _p4(rank_price, e0) is True)
    legs["p5_faithfulness_and_floor_both_models"] = (
        _p5(env_price, e0) is True and _p5(rank_price, e0) is True)
    legs["p6_set_pricing_counting_measure_kept"] = (_p6(e0) is True)
    # text <-> executable value tie (third-audit MAJOR-2): each
    # boundary phrase, as written in P_FROZEN, is asserted verbatim,
    # and the matching _p* executable is exercised AT that boundary by
    # value on witness pricers: a conforming witness at the boundary
    # passes, out-of-boundary witnesses fail.  P-6 takes no candidate
    # pricer (model-independent by construction); its numeric content
    # is exercised inside _p6.
    tok_ok = ("c(E_ii) = eps" in P_FROZEN["P-1"]
              and "c(E_ij) = eps" in P_FROZEN["P-2"]
              and "c(x + y) = c(x) + c(y)" in P_FROZEN["P-3"]
              and "scales linearly in the unit eps" in P_FROZEN["P-4"]
              and "c(x) = 0 iff x = 0" in P_FROZEN["P-5"]
              and "c(x) >= eps" in P_FROZEN["P-5"])
    conforming = lambda x, n, e: e * supp_size(x)
    doubled = lambda x, n, e: 2 * e * supp_size(x)
    halved = lambda x, n, e: e * supp_size(x) / 2
    zeroed = lambda x, n, e: e * max(supp_size(x) - 1, 0)
    negated = lambda x, n, e: -e * supp_size(x) / 2
    eps_blind = lambda x, n, e: F(supp_size(x))
    superadd = lambda x, n, e: e * supp_size(x) ** 2
    linearf = lambda x, n, e: e * sum(v for row in x for v in row)
    u01 = unit_matrix(3, 0, 1)
    xl, yl = cellmat(3, [(0, 1, 1)]), cellmat(3, [(0, 1, -1)])
    boundary_values = (
        conforming(u01, 3, e0) == e0
        and doubled(u01, 3, e0) == 2 * e0
        and F(0) < halved(u01, 3, e0) < e0
        and zeroed(u01, 3, e0) == 0
        and -e0 < negated(u01, 3, e0) < F(0)
        and linearf(madd(xl, yl, 3), 3, e0)
            == linearf(xl, 3, e0) + linearf(yl, 3, e0))
    predicate_ties = (
        _p1(conforming, e0) is True and _p2(conforming, e0) is True
        and _p1(doubled, e0) is False and _p2(doubled, e0) is False
        and _p1(halved, e0) is False and _p2(halved, e0) is False
        and _p3(conforming, e0) is True and _p3(superadd, e0) is False
        and _p4(conforming, e0) is True and _p4(eps_blind, e0) is False
        and _p5(conforming, e0) is True
        and _p5(halved, e0) is False
        and _p5(negated, e0) is False
        and _p5(zeroed, e0) is False
        and _p7(linearf, e0) is False)
    legs["p_texts_tied_to_executables_boundary"] = (
        tok_ok and boundary_values and predicate_ties)
    return _result("check_T_p_battery_both_models", legs, fails,
                   {"properties_checked": ["P-1", "P-2", "P-3", "P-4",
                                           "P-5", "P-6"],
                    "models": sorted(MODELS)})

def check_L_p7_banked_trio_claims_untouched():
    legs, fails = {}, []
    e0 = probed_eps()[0]
    trio_names = sorted(list(WORD_EXPECTED_LEGS) + list(ELL_EXPECTED_LEGS)
                        + list(MD_EXPECTED_LEGS))
    legs["trio_check_names_set_exact"] = (
        sorted(BANKED_CLAIMS_REVIEWED) == trio_names
        and len(trio_names) == 15
        and len(WORD_EXPECTED_LEGS) == 6
        and len(ELL_EXPECTED_LEGS) == 5
        and len(MD_EXPECTED_LEGS) == 4)
    cats = Counter(v[0] for v in BANKED_CLAIMS_REVIEWED.values())
    legs["reason_categories_valid_and_counts"] = (
        set(cats) == {"word-sector", "linear-family-conditioned",
                      "conditional_on_premise"}
        and cats["word-sector"] == 5
        and cats["linear-family-conditioned"] == 6
        and cats["conditional_on_premise"] == 4
        and sum(cats.values()) == 15
        and all(isinstance(v[1], str) and len(v[1]) > 0
                for v in BANKED_CLAIMS_REVIEWED.values()))
    x1, y1 = cellmat(3, [(0, 1, 1)]), cellmat(3, [(0, 1, -1)])
    x2, y2 = cellmat(3, [(0, 1, 1)]), cellmat(3, [(0, 2, 1)])
    legs["models_nonlinear_outside_linear_family"] = (
        env_price(x1, 3, e0) + env_price(y1, 3, e0) == 2 * e0
        and env_price(madd(x1, y1, 3), 3, e0) == 0
        and env_price(madd(x1, y1, 3), 3, e0)
            != env_price(x1, 3, e0) + env_price(y1, 3, e0)
        and rank_price(x2, 3, e0) + rank_price(y2, 3, e0) == 2 * e0
        and rank_price(madd(x2, y2, 3), 3, e0) == e0
        and rank_price(madd(x2, y2, 3), 3, e0)
            != rank_price(x2, 3, e0) + rank_price(y2, 3, e0))
    vals, _ = argmin_values(uniform_cost(3, e0), 6, "set",
                            closed_only=False)
    legs["word_sector_unit_agreement_complete_uniform"] = all(
        vals[(i, j)] == e0
        and env_price(unit_matrix(3, i, j), 3, e0) == vals[(i, j)]
        and rank_price(unit_matrix(3, i, j), 3, e0) == vals[(i, j)]
        for i in range(3) for j in range(3))
    # the referee's own predicates, run on declared records for BOTH
    # models (second-audit MINOR-3): the fixture inventory excludes the
    # models by name, the predicate rows are computed, and no fixture's
    # declared superposition rule reproduces either model's computed
    # price at the witness E_01 + E_02
    fx = _referee_fixtures(e0)
    model_uv = {(i, j): e0 for i in range(3) for j in range(3)}
    recs = {}
    for mname, pfn in (("M_ENV", env_price), ("M_RANK", rank_price)):
        recs[mname] = {
            "structure_price": lambda S: e0 * len(S),
            "unit_values": {(i, j): pfn(unit_matrix(3, i, j), 3, e0)
                            for i in range(3) for j in range(3)},
            "superposition": None,
            "premises": set(PREMISES_CONSUMED),
        }
    rows = {mname: _referee_predicates(mname, rec, e0)
            for mname, rec in recs.items()}
    xw = cellmat(3, [(0, 1, 1), (0, 2, 1)])
    sup_ok = True
    for cand in fx.values():
        sup = cand["superposition"]
        if sup is not None:
            v = sup[0](0, 1)
            sup_ok = (sup_ok and v != env_price(xw, 3, e0)
                      and v != rank_price(xw, 3, e0))
    legs["referee_predicates_run_on_model_records"] = (
        len(fx) == 9
        and not ({"M_ENV", "M_RANK"} & set(fx))
        and all(recs[m]["unit_values"] == model_uv for m in recs)
        and rows["M_ENV"] == rows["M_RANK"]
            == {"a": True, "b": False, "c1": True, "c2": False,
                "d": True}
        and sup_ok
        and env_price(xw, 3, e0) == 2 * e0
        and rank_price(xw, 3, e0) == e0)
    md_rec = _md_premise_check()
    legs["md_residual_data_tied"] = (
        MD_RESIDUAL_PREMISES == frozenset({"MD_SUPER_NODISCOUNT"})
        and MD_RESIDUAL_PREMISES <= MD_PREMISES_CONSUMED
        and md_rec["passed"] is True
        and md_rec["conditional_on"] == ["MD_SUPER_NODISCOUNT"]
        and "MD_SUPER_NODISCOUNT" not in PREMISES_CONSUMED)
    return _result("check_L_p7_banked_trio_claims_untouched", legs, fails,
                   {"trio_checks_reviewed": len(BANKED_CLAIMS_REVIEWED),
                    "category_counts": dict(cats)})

# ---------------------------------------------------------------------------
# the separation and the two verdicts
# ---------------------------------------------------------------------------

def check_T_separation_and_two_verdicts():
    legs, fails = {}, []
    e0 = probed_eps()[0]
    doms = {n: two_set_domain(n) for n in (3, 4)}
    # domain shape: counts and per-set sign-tuple completeness
    dc_ok = (len(doms[3]) == 60 and len(doms[4]) == 264
             and len({S for S, _, _ in doms[3]}) == 15
             and len({S for S, _, _ in doms[4]}) == 66)
    for n in (3, 4):
        per_set = {}
        for S, signs, _ in doms[n]:
            per_set.setdefault(S, set()).add(signs)
        dc_ok = dc_ok and all(
            sg == {(1, 1), (1, -1), (-1, 1), (-1, -1)}
            for sg in per_set.values())
    legs["domain_counts_and_sign_tuples_complete"] = dc_ok
    # the spec's separation instance, both signs
    xs = {sgn: signed_combo(3, ((0, 1), (0, 2)), (1, sgn))
          for sgn in (1, -1)}
    legs["e01_pm_e02_both_signs_values"] = (
        xs[1] != xs[-1]
        and all(env_price(x, 3, e0) == 2 * e0
                and rank_price(x, 3, e0) == e0
                and matrix_rank(x) == 1 and supp_size(x) == 2
                and rank_price(x, 3, e0) < env_price(x, 3, e0)
                for x in xs.values()))
    # tie by value to the md_super sibling's N1 rows: same (S, signs)
    # enumeration set-exactly, and c_env equals each row's constant part
    tie_ok = True
    for n in (3, 4):
        rows, _ = nodiscount_system(n, e0)
        tie_ok = (tie_ok
                  and {(S, signs) for _, _, S, signs in rows}
                      == {(S, signs) for S, signs, _ in doms[n]}
                  and len(rows) == len(doms[n])
                  and all(env_price(signed_combo(n, S, signs), n, e0)
                          == const
                          for _, const, S, signs in rows))
    legs["env_center_price_tie_to_n1_rows"] = tie_ok
    # verdict in M-ENV: true at every instance, with equality (zero slack)
    env_ok, env_viol_counts = True, []
    for n in (3, 4):
        vals = [env_price(x, n, e0) for _, _, x in doms[n]]
        env_viol_counts.append(sum(1 for v in vals if v < 2 * e0))
        env_ok = (env_ok and len(vals) == len(doms[n])
                  and all(v >= 2 * e0 for v in vals)
                  and vals == [2 * e0] * len(doms[n]))
    legs["md_super_true_in_env_zero_slack"] = env_ok
    # verdict in M-RANK: false, at exactly the rank-deficient instances
    viol_counts, rk_ok = [], True
    for n in (3, 4):
        viol = [(S, signs) for S, signs, x in doms[n]
                if rank_price(x, n, e0) < 2 * e0]
        viol_counts.append(len(viol))
        rk_ok = (rk_ok
                 and all(rank_price(x, n, e0) == e0
                         for S, signs, x in doms[n]
                         if (S, signs) in set(viol))
                 and all(rank_price(x, n, e0) == 2 * e0
                         for S, signs, x in doms[n]
                         if (S, signs) not in set(viol))
                 and len(viol) > 0)
    legs["md_super_false_in_rank_with_counts"] = (
        rk_ok and viol_counts == [24, 96])
    # the full signed source-sharing family, per instance
    fam_ok, fam_counts = True, []
    for n in (3, 4):
        fam = [(S, signs, x) for S, signs, x in doms[n]
               if len({a for (a, b) in S}) == 1]
        fam_counts.append(len(fam))
        fam_ok = (fam_ok and len({S for S, _, _ in fam})
                      == n * (n - 1) * (n - 2) // 2
                  and all(env_price(x, n, e0) == 2 * e0
                          and rank_price(x, n, e0) == e0
                          and any(matmul(mt(x, n), x, n)[i][j] != 0
                                  for i in range(n) for j in range(n)
                                  if i != j)
                          for _, _, x in fam))
    legs["source_sharing_family_per_instance"] = (
        fam_ok and fam_counts == [12, 48])
    # the two MODELS verdict strings, tied by VALUE to the counted
    # violations: a zero count yields "HOLDS", a positive count yields
    # "FAILS" (second-audit MINOR-2)
    env_word = "HOLDS" if sum(env_viol_counts) == 0 else "FAILS"
    rank_word = "HOLDS" if sum(viol_counts) == 0 else "FAILS"
    legs["model_verdict_strings_tied_to_counts"] = (
        env_viol_counts == [0, 0]
        and viol_counts == [24, 96]
        and env_word != rank_word
        and MODELS["M_ENV"]["md_super_verdict"].startswith(env_word)
        and MODELS["M_RANK"]["md_super_verdict"].startswith(rank_word))
    # key_result verdicts are the computed words themselves, tied to
    # the counts in the model_verdict_strings leg (third-audit MINOR-3)
    return _result("check_T_separation_and_two_verdicts", legs, fails,
                   {"domain_sizes": [len(doms[3]), len(doms[4])],
                    "env_violation_counts": env_viol_counts,
                    "rank_violation_counts": viol_counts,
                    "source_sharing_instances": fam_counts,
                    "env_verdict": env_word,
                    "rank_verdict": rank_word})

def check_L_atom_admissibility_and_bridge():
    legs, fails = {}, []
    e0 = probed_eps()[0]
    # inclusion: every signed envelope atom is rank one
    inc_ok, inc_counts = True, []
    for n in (3, 4):
        ats = env_atoms(n)
        inc_counts.append(len(ats))
        inc_ok = inc_ok and all(
            matrix_rank(a) == 1 and rank_by_minors(a) == 1 for a in ats)
    legs["env_atoms_are_rank_one_inclusion"] = (
        inc_ok and inc_counts == [18, 32])
    # pointwise dominance c_rank <= c_env with strict sites
    dom_all = (signed_presentations(3, 3) + signed_presentations(4, 3))
    dom_ns = [3] * 834 + [4] * 4992
    strict = 0
    dom_ok = len(dom_all) == 5826
    for n, x in zip(dom_ns, dom_all):
        rp, ep = rank_price(x, n, e0), env_price(x, n, e0)
        dom_ok = dom_ok and rp <= ep
        if rp < ep:
            strict += 1
    lg_ok = all(rank_price(cellmat(n, ent), n, e0)
                <= env_price(cellmat(n, ent), n, e0)
                for n, ent, _, _ in LARGER_SAMPLES)
    legs["pointwise_dominance_with_strict_sites"] = (
        dom_ok and lg_ok and strict > 0 and strict < len(dom_all))
    # divergence on the 2-set domain == rank-deficiency == shared
    # source or shared target
    div_ok, div_counts = True, []
    doms = {n: two_set_domain(n) for n in (3, 4)}
    for n in (3, 4):
        div = {(S, signs) for S, signs, x in doms[n]
               if rank_price(x, n, e0) < env_price(x, n, e0)}
        rk_def = {(S, signs) for S, signs, x in doms[n]
                  if matrix_rank(x) < 2}
        shared = {(S, signs) for S, signs, _ in doms[n]
                  if len({a for (a, b) in S}) == 1
                  or len({b for (a, b) in S}) == 1}
        div_counts.append(len(div))
        div_ok = div_ok and div == rk_def == shared and len(div) > 0
    legs["divergence_exactly_rank_deficient"] = (
        div_ok and div_counts == [24, 96])
    # N1's binding sets: exactly the source-sharing sets, a strict
    # subset of the divergence sites, every one divergent
    bind_ok, bind_counts = True, []
    for n in (3, 4):
        rows, _ = nodiscount_system(n, e0)
        binding = {(S, signs) for coeff, _, S, signs in rows
                   if any(c != 0 for c in coeff)}
        src = {(S, signs) for S, signs, _ in doms[n]
               if len({a for (a, b) in S}) == 1}
        div = {(S, signs) for S, signs, x in doms[n]
               if rank_price(x, n, e0) < env_price(x, n, e0)}
        bind_counts.append(len(binding))
        bind_ok = (bind_ok and binding == src
                   and binding < div
                   and all(rank_price(signed_combo(n, S, signs), n, e0)
                           < env_price(signed_combo(n, S, signs), n, e0)
                           for S, signs in binding))
    legs["n1_binding_sets_source_sharing_divergent_subset"] = (
        bind_ok and bind_counts == [12, 48]
        and div_counts == [2 * c for c in bind_counts])
    # the load-semantics bridge: rank(x^T x) = rank(x) on every sample
    bridge_items = ([(3, x) for x in signed_presentations(3, 3)]
                    + [(4, x) for x in signed_presentations(4, 3)]
                    + [(3, x) for _, _, x in doms[3]]
                    + [(4, x) for _, _, x in doms[4]]
                    + [(n, cellmat(n, ent))
                       for n, ent, _, _ in LARGER_SAMPLES])
    br_ok = len(bridge_items) == 834 + 4992 + 60 + 264 + 5
    for n, x in bridge_items:
        br_ok = br_ok and matrix_rank(matmul(mt(x, n), x, n)) \
            == matrix_rank(x)
    legs["bridge_rank_xtx_equals_rank_x"] = br_ok
    return _result("check_L_atom_admissibility_and_bridge", legs, fails,
                   {"dominance_strict_sites": strict,
                    "divergence_counts": div_counts,
                    "binding_counts": bind_counts,
                    "bridge_instances": len(bridge_items),
                    "identification": "same argmin, two atom sets; "
                                      "atom-set inclusion gives "
                                      "pointwise c_rank <= c_env"})

# ---------------------------------------------------------------------------
# the independence conclusion
# ---------------------------------------------------------------------------

def check_T_independence_conclusion_record():
    legs, fails = {}, []
    e0 = probed_eps()[0]
    pids = sorted(P_FROZEN)
    legs["p_frozen_set_exact_and_not_in_p"] = (
        pids == ["P-1", "P-2", "P-3", "P-4", "P-5", "P-6", "P-7"]
        and all(isinstance(v, str) and len(v) > 0
                for v in P_FROZEN.values())
        and hashlib.sha256(
            "\n".join(k + ": " + P_FROZEN[k]
                       for k in pids).encode("utf-8")
        ).hexdigest() == P_FROZEN_SHA256
        and NOT_IN_P == frozenset({"FUNCTIONAL_LINEARITY"})
        and not (NOT_IN_P & set(P_FROZEN)))
    table = {(m, p): _p_cell(m, p, e0)
             for m in sorted(MODELS) for p in pids}
    legs["model_property_table_all_cells_computed"] = (
        sorted(table) == sorted((m, p) for m in ("M_ENV", "M_RANK")
                                for p in pids)
        and len(table) == 14
        and all(v is True for v in table.values()))
    viol3 = [1 for S, signs, x in two_set_domain(3)
             if rank_price(x, 3, e0) < 2 * e0]
    legs["not_entailed_witnessed_by_rank_model"] = (
        all(table[("M_RANK", p)] is True for p in pids)
        and sum(viol3) == 24 and sum(viol3) > 0
        and CONCLUSION["not_entailed_by_P"] is True
        and CONCLUSION["witness_not_entailed"] == "M_RANK")
    env_vals = [env_price(x, 3, e0) for _, _, x in two_set_domain(3)]
    legs["not_refuted_witnessed_by_env_model"] = (
        all(table[("M_ENV", p)] is True for p in pids)
        and len(env_vals) == 60
        and all(v >= 2 * e0 for v in env_vals)
        and sum(1 for v in env_vals if v < 2 * e0) == 0
        and CONCLUSION["not_refuted_by_P"] is True
        and CONCLUSION["witness_not_refuted"] == "M_ENV")
    # scope, computed: signed entries only; complete uniform carrier
    dom3 = signed_presentations(3, 3)
    signed_ok = all(v in (F(1), F(-1), F(0))
                    for x in dom3 for row in x for v in row)
    signed_ok = signed_ok and all(
        v in (F(1), F(-1), F(0))
        for _, _, x in two_set_domain(3) for row in x for v in row)
    uc = uniform_cost(3, e0)
    legs["scope_fields_computed"] = (
        sorted(CONCLUSION) == ["not_entailed_by_P", "not_refuted_by_P",
                               "scope", "witness_not_entailed",
                               "witness_not_refuted"]
        and sorted(SCOPE) == ["bridge", "carrier", "coefficients"]
        and signed_ok
        and set(uc) == set(all_pairs(3))
        and all(v == e0 for v in uc.values()))
    legs["premise_inventory_set_exact"] = (
        sorted(PREMISES_CONSUMED) == [
            "A2_ARGMIN", "CARRIER_COMPLETENESS", "DEF_APS_STRUCTURE_COST",
            "EQUAL_COST_UNIFORMITY", "FD3_FLOOR", "FD4_FINITE_CARRIER",
            "LINEAR_REALIZATION_TARGET",
            "NONEMPTY_ENFORCEMENT_PRESENTATION",
        ]
        and PREMISES_CONSUMED == frozenset(WORD_PREMISES_CONSUMED)
        and sorted(PREMISES_NOT_CONSUMED) == [
            "CYCLICITY", "DET_MAX_SELECTION_PRINCIPLE",
            "FUNCTIONAL_LINEARITY", "MD_SUPER_NODISCOUNT",
            "MISSING_LEMMA_EQUALITY_AS_PREMISE",
            "P1_SANDWICH_REALIZATION", "P2_PRESENTATION_GAUGE",
            "P3_UNDERIVED", "PHI_EQ_EPS_TR_STIPULATION",
            "REAL_SYMMETRIC_TEST_SECTOR",
        ]
        and not (PREMISES_CONSUMED & PREMISES_NOT_CONSUMED)
        and OBJECT_OF_STUDY == frozenset({"MD_SUPER_NODISCOUNT"})
        and OBJECT_OF_STUDY <= PREMISES_NOT_CONSUMED
        and CONDITIONAL_ON == [])
    return _result("check_T_independence_conclusion_record", legs, fails,
                   {"table_cells": len(table),
                    "rank_violations_n3": sum(viol3),
                    "env_violations_n3": 0,
                    "conclusion": dict(CONCLUSION,
                                       scope=dict(SCOPE))})

# ---------------------------------------------------------------------------
# the scope fence
# ---------------------------------------------------------------------------

def check_L_scope_fence_and_nonlinearity():
    legs, fails = {}, []
    e0 = probed_eps()[0]
    # off the complete carrier both models diverge from banked psi_min:
    # the P3 path prices E_02 at 2*eps by word distance
    p3 = {frozenset((0, 1)): e0, frozenset((1, 2)): e0}
    vals_p3, _ = argmin_values(p3, 6, "set", closed_only=False)
    u02 = unit_matrix(3, 0, 2)
    legs["p3_carrier_divergence_reason"] = (
        vals_p3[(0, 2)] == 2 * e0
        and env_price(u02, 3, e0) == e0
        and rank_price(u02, 3, e0) == e0
        and env_price(u02, 3, e0) != vals_p3[(0, 2)]
        and rank_price(u02, 3, e0) != vals_p3[(0, 2)])
    # control: on the complete uniform carrier both models agree with
    # psi_min on every unit
    vals_c, _ = argmin_values(uniform_cost(3, e0), 6, "set",
                              closed_only=False)
    legs["complete_carrier_agreement_control"] = all(
        vals_c[(i, j)] == e0
        and env_price(unit_matrix(3, i, j), 3, e0) == vals_c[(i, j)]
        and rank_price(unit_matrix(3, i, j), 3, e0) == vals_c[(i, j)]
        for i in range(3) for j in range(3))
    # non-linearity witnesses (neither model is a linear functional)
    x1, y1 = cellmat(3, [(0, 1, 1)]), cellmat(3, [(0, 1, -1)])
    legs["nonlinearity_witness_env"] = (
        env_price(x1, 3, e0) == e0 and env_price(y1, 3, e0) == e0
        and env_price(madd(x1, y1, 3), 3, e0) == 0
        and env_price(madd(x1, y1, 3), 3, e0)
            != env_price(x1, 3, e0) + env_price(y1, 3, e0))
    x2, y2 = cellmat(3, [(0, 1, 1)]), cellmat(3, [(0, 2, 1)])
    legs["nonlinearity_witness_rank"] = (
        rank_price(x2, 3, e0) == e0 and rank_price(y2, 3, e0) == e0
        and rank_price(madd(x2, y2, 3), 3, e0) == e0
        and rank_price(madd(x2, y2, 3), 3, e0)
            != rank_price(x2, 3, e0) + rank_price(y2, 3, e0)
        and rank_price(madd(x1, y1, 3), 3, e0) == 0)
    # the signed-unit-coefficient scope, verified over the domains used
    checked = 0
    ok = True
    for n in (3, 4):
        for x in signed_presentations(n, 3):
            checked += 1
            ok = ok and all(v in (F(1), F(-1), F(0))
                            for row in x for v in row)
    legs["signed_domain_verified"] = (ok and checked == 834 + 4992)
    return _result("check_L_scope_fence_and_nonlinearity", legs, fails,
                   {"p3_psi_min_E02": str(vals_p3[(0, 2)]),
                    "model_price_E02": str(env_price(u02, 3, e0)),
                    "signed_domain_checked": checked})

# ---------------------------------------------------------------------------

ALL_CHECKS = [
    check_T_env_closed_form_support_pricing,
    check_T_rank_closed_form_rank_pricing,
    check_T_p_battery_both_models,
    check_L_p7_banked_trio_claims_untouched,
    check_T_separation_and_two_verdicts,
    check_L_atom_admissibility_and_bridge,
    check_T_independence_conclusion_record,
    check_L_scope_fence_and_nonlinearity,
]

def run_all():
    results = []
    for fn in ALL_CHECKS:
        r = fn()
        results.append(r)
        status = "PASS" if r["passed"] else "FAIL"
        n_true = sum(1 for v in r["legs"].values() if v is True)
        print(f"[{status}] {r['name']}  legs={n_true}/{len(r['legs'])}")
        if not r["passed"]:
            for f in r["fails"]:
                print("   -", f)
    print(f"{sum(r['passed'] for r in results)}/{len(results)} checks pass")
    return results

# ---------------------------------------------------------------------------
# registration -- BARE-name keys per the 2026-08-03 D6 ruling (canonical for
# new modules; by-name gates check both spellings)
# ---------------------------------------------------------------------------

_CHECKS = {
    'T_env_closed_form_support_pricing':
        check_T_env_closed_form_support_pricing,
    'T_rank_closed_form_rank_pricing':
        check_T_rank_closed_form_rank_pricing,
    'T_p_battery_both_models': check_T_p_battery_both_models,
    'L_p7_banked_trio_claims_untouched':
        check_L_p7_banked_trio_claims_untouched,
    'T_separation_and_two_verdicts': check_T_separation_and_two_verdicts,
    'L_atom_admissibility_and_bridge': check_L_atom_admissibility_and_bridge,
    'T_independence_conclusion_record':
        check_T_independence_conclusion_record,
    'L_scope_fence_and_nonlinearity': check_L_scope_fence_and_nonlinearity,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


if __name__ == "__main__":
    run_all()
