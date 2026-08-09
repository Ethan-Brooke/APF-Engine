"""The FD3-valuation Born chain: the protocol infimum, computed, and what it forces.

Built 2026-08-04 by a cold build seat from
``Artifacts_2026-08-04_session/fd3_born_chain_build/
BUILD_SPEC_fd3_valuation_born_chain_2026-08-04.md``; parent charter
``Reference - CHARTER - Deriving or Refuting MD-Super-Nodiscount
(2026-08-04)``, Branch D horn, executed ON TOP OF the landed Branch N
independence result.

AUDIT RECORD (all 2026-08-04): audit 1 blinded cold, LAND-WITH-FIXES
0.85; audit 2 blinded cold, LAND-WITH-FIXES 0.87; audit 3 blinded cold,
LAND-WITH-FIXES 0.87; fixes carried by separate cold fix seats after
each round.  All audits were blinded cold seats under the retired
different-day convention (ruling: ``Reference - DECISION - Retiring the
Different-Day Audit Convention (2026-08-04)``).  Banked as v24.3.466
(2026-08-04).

------------------------------------------------------------------------------
WHAT THIS MODULE COMPUTES (exact arithmetic; stdlib + fractions; shared
machinery imported from the banked v24.3.465 trio and from the
sha-pinned independence-witness sibling, not duplicated)
------------------------------------------------------------------------------

The corpus prices a realized object by the infimum of admissible
substrate-protocol cost (FD3 via the infimum-over-admissible-protocols
valuation convention -- stated in a docstring inside
``check_T_PLEC_derived_from_spine``, ``apf/foundation_inputs.py``, and
exercised there on a toy witness; Paper 10 v1.23 operational form; a
NAMED PREMISE, carried in ``conditional_on`` -- RULED 2026-08-04).
This module evaluates that valuation on the word
protocols the carrier can write, under two NAMED DEFINITIONAL CLAUSES
(module data NAMED_CLAUSES; consumed, never derived), and computes the
chain that results.  Scope throughout: complete uniform carrier, signed
unit coefficients, symmetric slice.

THE TWO NAMED CLAUSES (spec Sec. 2; definitions, not theorems; carried
in ``conditional_on`` on every returned record together with
FD3_VALUATION_CONVENTION and the standing LINEAR_REALIZATION_TARGET
residual):

  DEF_REALIZATION_SIGNED_CONTRACTION.  A protocol is a finite multiset
  of (sign, word) pairs, e_i in {+1,-1}, w_i an admissible word (walk)
  on the carrier; it REALIZES the algebra element x iff
  sum_i e_i * pi(w_i) = x (pi the banked contraction map,
  word_carrier_transfer); its cost is sum_i price(w_i) (def:aps-shaped
  additive pricing, SET mode, via the banked pricing machinery).  This
  is the middle reading of the empty-fiber fork; the two excluded
  alternatives are RECORDED as module data EXCLUDED_ALTERNATIVES, each
  with a computed disagreement at C4: the strict pole (empty word fiber
  => unpriceable) and the permissive pole (superposed atoms admitted),
  the permissive pole with the rank model as its standing witness
  (md_super_independence_witness).

  COST_REPRESENTATION_ON_LOADS.  The linear functional phi representing
  enforcement cost on the symmetric test sector agrees with the FD3
  valuation on the load family: phi(x^T x) = c(x) for the signed
  separator combinations in scope.  (Clause (i) of the old MD-super
  residual, carried as an explicit definitional bridge instead of
  hiding inside an inequality.)

C1 -- THE VALUATION CLOSED FORM (check_T_fd3_valuation_closed_form).
Under DEF_REALIZATION: c(x) = eps * |supp(x)| for signed
unit-coefficient x.  Two-sided, computed exhaustively at n = 3 and 4
over every signed presentation with support <= 3 (834 and 4992), plus
sampled n = 5 cases, at two eps scales tied by value.  Lower bound:
every enumerated word contracts to a single matrix unit and is priced
>= eps, with the per-cell fiber minimum exactly eps (tied by value to
the banked argmin_values), so a protocol of m words realizes an element
of support <= m at cost >= m*eps >= |supp|*eps.  The step past the
enumeration to words of ANY length is the nonempty-support fact: every
word has at least one edge and SET pricing charges every edge >= eps,
so every word of every length is priced >= eps -- the computed
every-word->=eps leg instantiates this bound on the enumeration, and
the closed form is the infimum over ALL protocols (unbounded word
length and multiset size).  Upper bound: the
single-step cell protocol (length-1 word per off-diagonal cell, 2-step
loop per diagonal cell) attains eps per cell.  The CANCELLATION CASE is
its own leg: over the full protocol enumeration at n = 3 (multisets of
size <= 3 over all signed length-<=2 words, 9138 protocols), every
protocol that covers a cell outside the support of its realized element
hits each such cell an even number >= 2 of times with sign-sum zero,
has size >= |supp| + 2, and is STRICTLY costlier than eps * |supp|.
The exhaustive protocol argmin table at n = 3 equals the closed form on
all 834 presentations; at n = 4 minimal protocol SIZE equals support on
all 4992 (reachability sets at sizes 1 and 2, attainment at 3).

C2 -- MD-SUPER, WITH EQUALITY, UNDER COST_REPRESENTATION_ON_LOADS
(check_T_md_super_derived_with_equality).  The derivation step is the
definitional identification phi(x^T x) := c(x): it is consumed, not
derived.  The registry key does not carry that qualifier; the returned
record does, at ``derivation_step`` and in ``conditional_on``.
For x a signed combination of k distinct separators:
supp(x) = k (distinct ordered pairs are
distinct cells), so c(x) = k*eps by C1; under
COST_REPRESENTATION_ON_LOADS, phi(x^T x) = c(x) = k*eps >= k*eps -- the
no-discount inequality holds WITH EQUALITY, as a theorem of the full
C5 consumed ledger (twelve names, set-exact): the step-local premises
{FD3_VALUATION_CONVENTION, DEF_REALIZATION_SIGNED_CONTRACTION,
COST_REPRESENTATION_ON_LOADS} on top of C1's closed form, which
consumes the imported word-module scope premises.  Of the step-local
premises, FD3_VALUATION_CONVENTION is CONSUMED as a premise (it lives
in PREMISES_CONSUMED) AND carried in ``conditional_on`` (RULED
2026-08-04); its banked anchor is a docstring-stated
convention inside ``check_T_PLEC_derived_from_spine``
(``foundation_inputs.py``), a parenthetical exercised on a toy
witness, not a standalone registered statement (see the
``conditional_on`` note in-code); ``conditional_on`` carries the
three named clauses plus the standing linearity residual (spec
Sec. 2 + the 2026-08-04 ruling).  Computed over
every signed set of sizes
2 and 3 at n = 3 and 4 (60 + 160 and 264 + 1760 instances), at two eps
scales.  Tied by value to the banked ``md_super_nodiscount`` system:
the nodiscount_system (S, signs) enumeration equals this module's k = 2
domain SET-EXACTLY at n = 3 and 4, and every row's constant part equals
C1's valuation on that row's own signed set.

C3 -- THE CENTER FORCED, BORN PRICING RECOVERED
(check_T_center_forced_born_pricing).  Feeding the C2 equality into the
linear family W (symmetric, diag W = eps -- the elliptope's E1
parametrization): the equality system phi_W(x^T x) = k*eps over the C2
domain is HOMOGENEOUS (its inhomogeneity vanishes because the RHS *is*
the valuation: const = eps*Tr(x^T x) = k*eps = c(x), a computed value
tie -- the k-resolution equality is here an OUTPUT of the valuation,
not an input), and its coefficient matrix has kernel ZERO at n = 3 and
4 by a LOCAL Gaussian-elimination path (independent of the sibling's
axis-pair deduction, which is then cross-checked by value:
forced_solution covers every unknown and forces zero).  Solution set on
the symmetric slice = { W = eps*I }; at the center the functional is
exactly eps*Tr on every sample element (with a non-forced-off-diagonal
control that disagrees), and every off-diagonal perturbation breaks the
equality on at least one instance.

C4 -- THE EXCLUSION RECORD
(check_L_rank_model_excluded_no_superposed_image).  The rank model is
NOT an FD3 valuation under DEF_REALIZATION: c_rank(E_01 + E_02) = eps
< 2*eps = the protocol infimum (both computed; the infimum from the
exhaustive C1 table).  More generally no infimum over realizing word
protocols prices a signed k-set below k*eps -- that IS C1's lower
bound, verified over every k = 2, 3 signed set at n = 3 and every
k = 2 set at n = 4.  The permissive pole requires atoms no substrate
operation contracts to, computed: the word image at n = 3, 4 (every
word to length 6, 378 and 4368 words) is EXACTLY the set of matrix
units -- it contains no superposed element; E_01 +- E_02 is rank one
but outside the image.  The strict pole gets its own computed
disagreement: the superposed witness pair has an EMPTY signed
single-word fiber (outside the signed word image) while the adopted
valuation prices each at the finite protocol infimum 2*eps, so the
strict pole's unpriceable verdict and the computed table disagree on a
named instance.  The witness module supplying the rank
model is sha256-pinned as a leg.

C5 -- THE RESIDUAL LEDGER (check_L_residual_ledger_retirement).  A
computed record stating, set-exactly: what the chain CONSUMES
({FD3_VALUATION_CONVENTION, DEF_REALIZATION_SIGNED_CONTRACTION,
COST_REPRESENTATION_ON_LOADS, LINEAR_REALIZATION_TARGET} + the imported
word-module premises + the elliptope module's
REAL_SYMMETRIC_TEST_SECTOR); what it RETIRES as an independent premise --
MD_SUPER_NODISCOUNT, derived at C2, carried in PREMISES_NOT_CONSUMED
with the explicit DERIVED_HERE marker and cross-checked by name against
the trio's ``conditional_on`` fields (the md_super sibling's records
carry exactly that name); and what it does NOT touch (the linearity
residual itself -- LINEAR_REALIZATION_TARGET is consumed and carried in
conditional_on, not discharged; P1/P2/P3; CYCLICITY; the division-ring
selection).  A fresh own-emitted record is read back as a leg: its
``conditional_on`` equals the four-name conditional set by value
(record-level carry; audit 3 MAJOR-1).

C6 -- SCOPE FENCES (check_L_scope_fences).  The complete-uniform-
carrier fence with its computed REASON (on the path P3 the banked
psi_min prices E_02 at 2*eps by word distance while the valuation's
closed form gives eps -- recomputed here); the signed-unit-coefficient
domain verified entry-by-entry; the symmetric slice (every load x^T x
is symmetric and every antisymmetric coefficient matrix scores zero on
every load, with a nonzero control).

READING, in this docstring and in NO leg and NO returned field:
DEF_REALIZATION_SIGNED_CONTRACTION is the carrier transfer -- as a
DEFINITION.  The carrier gap is not closed; it is CROSSED BY DEFINITION
at DEF_REALIZATION -- the definition is the crossing, named, with the
excluded alternatives on record.  The honest sentence for the chain's
conclusion: Born pricing follows from three named clauses
(FD3_VALUATION_CONVENTION, DEF_REALIZATION_SIGNED_CONTRACTION,
COST_REPRESENTATION_ON_LOADS) plus the standing residuals.  Every
stronger sentence is on the MAY-NOT-CITE list below.

eps NOTE (the siblings' note, carried): eps enters only through the
word module's probed_eps() singleton probe on the banked
``symmetry_cost_floor.config_cost``.  An extensionally correct bypass
of the probe is invisible BY EXTENSIONALITY; at the unit probe eps = 1,
so a value-equal literal substituted for eps is likewise invisible.
The scaled re-runs (factor 3) are leg content: each consuming leg
asserts the scales are distinct and the values tie by factor.

------------------------------------------------------------------------------
PREMISES, SET-EXACT (carried as data below; declarations, audited from
outside, not self-enforced)
------------------------------------------------------------------------------
CONSUMED: FD3_VALUATION_CONVENTION (the corpus's
infimum-over-admissible-protocols valuation, F2 of the spec's reading
walk; banked anchor: a docstring parenthetical in foundation_inputs.py;
carried in ``conditional_on`` as a named premise, RULED 2026-08-04,
see the note in-code); DEF_REALIZATION_SIGNED_CONTRACTION and
COST_REPRESENTATION_ON_LOADS (the two named definitional clauses,
above); LINEAR_REALIZATION_TARGET (the standing linearity residual --
consumed and carried, not discharged); plus the imported word-module
inventory: A2_ARGMIN, FD3_FLOOR, FD4_FINITE_CARRIER,
DEF_APS_STRUCTURE_COST, EQUAL_COST_UNIFORMITY, CARRIER_COMPLETENESS,
NONEMPTY_ENFORCEMENT_PRESENTATION; plus the elliptope module's
REAL_SYMMETRIC_TEST_SECTOR (the symmetric test sector -- the slice
C3's quantifier runs over and C6 computes; imported alongside the
elliptope machinery, as the md_super sibling carries it).
NOT CONSUMED: MD_SUPER_NODISCOUNT -- RETIRED as an independent premise,
with the DERIVED_HERE marker (derived at C2 from the consumed set; the
trio consumes it as its named residual, this module does not);
MISSING_LEMMA_EQUALITY_AS_PREMISE (the equality is C1+C2's output);
PHI_EQ_EPS_TR_STIPULATION (the trace form is forced at C3, not
declared); and the untouched set P1_SANDWICH_REALIZATION,
P2_PRESENTATION_GAUGE, P3_UNDERIVED, CYCLICITY,
DIVISION_RING_SELECTION.

MAY NOT CITE (spec Sec. 4; in-module and for every downstream quote):
- "Born is derived" WITHOUT the conditional clause.  The honest
  sentence: Born pricing follows from three named clauses
  (FD3_VALUATION_CONVENTION, DEF_REALIZATION_SIGNED_CONTRACTION,
  COST_REPRESENTATION_ON_LOADS) plus the standing residuals.
- "The linearity residual is discharged."  It is consumed and carried
  in conditional_on on every record.
- "The carrier gap is closed."  It is CROSSED BY DEFINITION at
  DEF_REALIZATION -- the definition is the crossing, named, with the
  alternatives on record.
- "Clause (i) is derived."  COST_REPRESENTATION_ON_LOADS is named, not
  derived.
- "MD-super is FALSE."  Standing; the rank model is a model of the
  frozen base P, not of the world.
- Any sentence attributing content here to what the module PREVENTS.
  It computes; it does not prevent.
"""

import hashlib

from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from collections import defaultdict

from apf.word_carrier_transfer import (
    all_pairs, words_on, contraction, price, uniform_cost, unit_matrix,
    matmul, argmin_values, probed_eps,
    PREMISES_CONSUMED as WORD_PREMISES_CONSUMED,
)
from apf.carrier_elliptope import (
    mt, matrix_rank, sym_from_offdiag,
    PREMISES_CONSUMED as ELL_PREMISES_CONSUMED,
)
from apf.md_super_nodiscount import (
    separators, signed_combo, nodiscount_system, forced_solution, phi_of,
    PREMISES_CONSUMED as MD_PREMISES_CONSUMED,
    RESIDUAL_PREMISES as MD_RESIDUAL_PREMISES,
    check_L_premise_inventory_set_exact as _md_premise_check,
)
import apf.md_super_independence_witness as _witness
from apf.md_super_independence_witness import (
    supp_size, zmat, cellmat, madd, signed_presentations, rank_by_minors,
    rank_price,
)

# ---------------------------------------------------------------------------
# named clauses, premises, ledger data (C5 consumes these as data)
# ---------------------------------------------------------------------------

NAMED_CLAUSES = {
    "DEF_REALIZATION_SIGNED_CONTRACTION":
        "a protocol is a finite multiset of (sign, word) pairs, "
        "e_i in {+1,-1}, w_i an admissible word on the carrier; it "
        "realizes x iff sum_i e_i * pi(w_i) = x (pi the banked "
        "contraction map); its cost is sum_i price(w_i), def:aps SET "
        "pricing via the banked machinery",
    "COST_REPRESENTATION_ON_LOADS":
        "the linear functional phi representing enforcement cost on the "
        "symmetric test sector agrees with the FD3 valuation on the "
        "load family: phi(x^T x) = c(x) for the signed separator "
        "combinations in scope",
}

EXCLUDED_ALTERNATIVES = {
    "strict_pole": "empty word fiber => unpriceable (rejected reading "
                   "of the empty-fiber fork; computed disagreement at "
                   "C4: the superposed witness pair has an empty "
                   "signed single-word fiber yet a finite protocol "
                   "infimum)",
    "permissive_pole": "superposed atoms admitted; standing witness: "
                       "the rank model M_RANK "
                       "(md_super_independence_witness)",
}

# conditional_on = the chain's named premises: FD3_VALUATION_CONVENTION
# + the two named definitional clauses + the standing linearity
# residual.  RULED 2026-08-04: FD3_VALUATION_CONVENTION moved into
# conditional_on.
CONDITIONAL_ON = sorted(list(NAMED_CLAUSES)
                        + ["FD3_VALUATION_CONVENTION",
                           "LINEAR_REALIZATION_TARGET"])

PREMISES_CONSUMED = (frozenset(WORD_PREMISES_CONSUMED)
                     | frozenset(ELL_PREMISES_CONSUMED)
                     | frozenset(NAMED_CLAUSES)
                     | frozenset({"FD3_VALUATION_CONVENTION"}))
DERIVED_HERE = frozenset({"MD_SUPER_NODISCOUNT"})
NOT_TOUCHED = frozenset({
    "P1_SANDWICH_REALIZATION", "P2_PRESENTATION_GAUGE", "P3_UNDERIVED",
    "CYCLICITY", "DIVISION_RING_SELECTION",
})
PREMISES_NOT_CONSUMED = (NOT_TOUCHED | DERIVED_HERE | frozenset({
    "MISSING_LEMMA_EQUALITY_AS_PREMISE", "PHI_EQ_EPS_TR_STIPULATION",
}))

# the independence-witness sibling this module imports machinery from.
# Originally pinned at the post-FIX2 blob named in the build spec (F4),
# sha 4161940e...; RE-PINNED 2026-08-04 to the witness's post-third-audit
# fix blob (its own fix seat moved it the same day; provenance:
# Artifacts_2026-08-04_session/same_day_third_audits/
# md_super_independence_witness/FIX_RETURN...md, pre-banking sha
# 7286f438...); RE-PINNED again at the v24.3.466 banking wiring
# (2026-08-04): filename md_super_independence_witness.py, audit-record
# docstring + register() added -- the imported machinery is
# computationally unchanged by that wiring.  Current banked blob:
WITNESS_SHA256 = (
    "90d552a9d43cf535a9b02a6f3a897a73a54cdbc23fdd5fb827aa33a64c4adb93")

# ---------------------------------------------------------------------------
# protocol machinery (DEF_REALIZATION_SIGNED_CONTRACTION, executable)
# ---------------------------------------------------------------------------

def word_cell(w):
    """The contraction cell of a word, local spelling; tied by value to
    the banked contraction map in C1's first leg."""
    return (w[0], w[-1])

def realize_protocol(protocol, n):
    """sum_i e_i * pi(w_i) as an exact n x n matrix; protocol is an
    iterable of (sign, word) pairs."""
    x = zmat(n)
    for e, w in protocol:
        a, b = word_cell(w)
        x[a][b] += F(e)
    return x

def protocol_cost(protocol, cost):
    """The DEF_REALIZATION cost: sum of the words' def:aps SET prices
    via the banked pricing machinery (independent path; the table
    builder bills through _bill)."""
    return sum(price(w, cost, "set") for _, w in protocol)

def _bill(prices, combo):
    """The table builder's billing path: additive over the multiset."""
    return sum(prices[t] for t in combo)

def cheap_signed_words(n, cost):
    """All signed words of length <= 2 on the carrier (the cheapest
    fiber representatives live here; computed in C1)."""
    return [(e, w) for w in words_on(cost, 2) for e in (1, -1)]

def cell_protocol(x, n):
    """The attaining witness: one cheapest word per nonzero cell --
    the length-1 word for an off-diagonal cell, the 2-step loop for a
    diagonal cell -- signed by the cell entry."""
    prot = []
    for i in range(n):
        for j in range(n):
            v = x[i][j]
            if v != 0:
                w = (i, j) if i != j else (i, (i + 1) % n, i)
                prot.append((int(v), w))
    return tuple(prot)

def mat_key(x):
    return tuple(tuple(row) for row in x)

def protocol_argmin_table(n, e0, kmax):
    """Exhaustive protocol argmin over multisets of size <= kmax of
    signed length-<=2 words: a dict realized-element -> minimal cost,
    plus the raw enumeration (size, cost, key, combo) for the
    cancellation scan."""
    cost = uniform_cost(n, e0)
    atoms = cheap_signed_words(n, cost)
    prices = [price(w, cost, "set") for _, w in atoms]
    table, meta = {}, []
    for k in range(1, kmax + 1):
        for combo in combinations_with_replacement(range(len(atoms)), k):
            x = zmat(n)
            for t in combo:
                e, w = atoms[t]
                a, b = word_cell(w)
                x[a][b] += F(e)
            c = _bill(prices, combo)
            key = mat_key(x)
            if key not in table or c < table[key]:
                table[key] = c
            meta.append((k, c, key, combo))
    return table, meta, atoms, prices

def fd3_price(x, n, e0):
    """C1's closed form for the DEF_REALIZATION valuation on the signed
    domain: eps * |supp(x)| (proved two-sidedly in
    check_T_fd3_valuation_closed_form)."""
    return e0 * supp_size(x)

def phi_load(x, n, e0):
    """COST_REPRESENTATION_ON_LOADS, executable: phi(x^T x) := c(x).
    The identification IS the named clause; it is consumed, not
    derived."""
    return fd3_price(x, n, e0)

def k_set_domain(n, k):
    """All signed k-element separator sets: (S, signs, x)."""
    seps = separators(n)
    dom = []
    for S in combinations(seps, k):
        for signs in product((1, -1), repeat=k):
            dom.append((S, signs, signed_combo(n, S, signs)))
    return dom

def gauss_rank(rows):
    """Rank over Q of a list of row vectors -- the LOCAL elimination
    path for C3: independent of the sibling's axis-pair deduction, but
    the same textbook elimination class as the imported matrix_rank, so
    the in-leg rank cross-check is same-family; the negative-pivot
    fixtures carry the discrimination."""
    A = [list(r) for r in rows]
    if not A:
        return 0
    ncols = len(A[0])
    rank = 0
    for c in range(ncols):
        piv = next((r for r in range(rank, len(A)) if A[r][c] != 0), None)
        if piv is None:
            continue
        A[rank], A[piv] = A[piv], A[rank]
        A[rank] = [v / A[rank][c] for v in A[rank]]
        for r in range(len(A)):
            if r != rank and A[r][c] != 0:
                A[r] = [a - A[r][c] * b for a, b in zip(A[r], A[rank])]
        rank += 1
    return rank

def equality_system(n, e0, ks, price_fn=fd3_price):
    """The C3 equality system over the linear family W = eps*I + w:
    phi_W(x^T x) = k*eps for every signed k-set, k in ks.  Returns
    (coeff_rows, consts, rhs, unknowns); the row equation is
    const + coeff.w = rhs, and the rhs list is built FROM THE VALUATION
    (price_fn, default fd3_price), so 'the equality is the valuation's
    output' is a computed value tie, not prose; the C3 homogeneity leg
    probes the price_fn dependence with a decoy price function."""
    unk = [(i, j) for i in range(n) for j in range(i + 1, n)]
    coeff_rows, consts, rhs = [], [], []
    for k in ks:
        for S, signs, x in k_set_domain(n, k):
            g = matmul(mt(x, n), x, n)
            consts.append(e0 * sum(g[i][i] for i in range(n)))
            coeff_rows.append([g[i][j] + g[j][i] for (i, j) in unk])
            rhs.append(price_fn(x, n, e0))
    return coeff_rows, consts, rhs, unk

def trace_of(M, n):
    return sum(M[i][i] for i in range(n))

# ---------------------------------------------------------------------------
# result plumbing: set-exact leg inventory enforced on the check path
# ---------------------------------------------------------------------------

EXPECTED_LEGS = {
    "check_T_fd3_valuation_closed_form": [
        "attaining_cell_protocol_exhaustive_n3_n4",
        "cancellation_overshoot_strictly_costlier",
        "every_word_single_cell_and_priced_at_least_eps",
        "protocol_argmin_exhaustive_n3_n4_matches_closed_form",
        "sampled_larger_cases_n5",
        "scaled_eps_argmin_and_closed_form_tied",
        "word_cell_ties_banked_contraction",
    ],
    "check_T_md_super_derived_with_equality": [
        "cost_representation_phi_equals_k_eps_with_equality",
        "derived_weak_form_zero_violations_zero_slack",
        "scaled_eps_two_scales_tied",
        "signed_k_sets_support_equals_k",
        "tie_by_value_to_banked_nodiscount_rows",
        "valuation_prices_k_sets_at_k_eps",
    ],
    "check_T_center_forced_born_pricing": [
        "center_functional_is_eps_trace_with_control",
        "equality_rhs_is_valuation_output_not_premise",
        "equality_system_kernel_zero_independent_gauss",
        "offdiagonal_perturbation_breaks_equality",
        "scaled_eps_center_scales",
        "sibling_forced_solution_value_tie",
    ],
    "check_L_rank_model_excluded_no_superposed_image": [
        "no_protocol_prices_signed_k_set_below_k_eps",
        "rank_atom_not_substrate_contractible",
        "rank_model_disagrees_with_protocol_infimum",
        "strict_pole_empty_signed_word_fiber_yet_protocol_priced",
        "witness_module_sha_pinned",
        "word_image_no_superposed_element",
    ],
    "check_L_residual_ledger_retirement": [
        "conditional_on_carries_four_clauses",
        "consumed_disjoint_from_not_consumed",
        "consumed_set_exact",
        "linearity_residual_carried_not_discharged",
        "not_consumed_set_exact_with_derived_here_marker",
        "own_emitted_record_carries_conditional_on",
        "retired_name_cross_checked_against_trio",
    ],
    "check_L_scope_fences": [
        "complete_uniform_carrier_control",
        "p3_divergence_fence_reason",
        "signed_unit_coefficient_domain",
        "symmetric_slice_antisymmetric_inert",
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
        "passed": not fails,
        "legs": dict(legs),
        "fails": list(fails),
        "key_result": key_result,
        "conditional_on": list(CONDITIONAL_ON),
        "tier": 3,
        "epistemic": "P_math",
        "status": "banked v24.3.466 (2026-08-04)",
    }

# ---------------------------------------------------------------------------
# C1
# ---------------------------------------------------------------------------

def check_T_fd3_valuation_closed_form():
    legs, fails = {}, []
    e0 = probed_eps()[0]
    # (a) the local cell spelling ties the banked contraction map on
    # every enumerated word, both sizes, counts pinned
    words = {n: words_on(uniform_cost(n, e0), 6) for n in (3, 4)}
    legs["word_cell_ties_banked_contraction"] = (
        len(words[3]) == 378 and len(words[4]) == 4368
        and all(word_cell(w) == contraction(w)
                for n in (3, 4) for w in words[n]))
    # (b) every word contracts to a single unit and is priced >= eps;
    # the per-cell fiber minimum is exactly eps (tied by value to the
    # banked argmin over the full enumeration AND to the minimum over
    # the length-<=2 words the table uses)
    single_ok, price_ok, fiber_ok = True, True, True
    for n in (3, 4):
        cost = uniform_cost(n, e0)
        for w in words[n]:
            m = realize_protocol([(1, w)], n)
            single_ok = single_ok and supp_size(m) == 1 \
                and m[word_cell(w)[0]][word_cell(w)[1]] == F(1)
            price_ok = price_ok and price(w, cost, "set") >= e0
        vals, _ = argmin_values(cost, 6, "set", closed_only=False)
        cheap_min = {}
        for w in words_on(cost, 2):
            c = price(w, cost, "set")
            cell = word_cell(w)
            if cell not in cheap_min or c < cheap_min[cell]:
                cheap_min[cell] = c
        fiber_ok = (fiber_ok
                    and sorted(vals) == sorted(cheap_min)
                    and all(vals[cell] == e0 == cheap_min[cell]
                            for cell in vals)
                    and len(vals) == n * n)
    legs["every_word_single_cell_and_priced_at_least_eps"] = (
        single_ok and price_ok and fiber_ok)
    # (c) attainment: the cell protocol realizes x at cost exactly
    # eps*|supp(x)|, exhaustively at n = 3 and 4, support <= 3
    att_ok, att_counts = True, []
    for n in (3, 4):
        cost = uniform_cost(n, e0)
        dom = signed_presentations(n, 3)
        att_counts.append(len(dom))
        for x in dom:
            prot = cell_protocol(x, n)
            att_ok = (att_ok
                      and realize_protocol(prot, n) == x
                      and len(prot) == supp_size(x)
                      and protocol_cost(prot, cost)
                          == fd3_price(x, n, e0)
                      and fd3_price(x, n, e0) == e0 * supp_size(x))
    legs["attaining_cell_protocol_exhaustive_n3_n4"] = (
        att_ok and att_counts == [834, 4992])
    # (d) the exhaustive protocol argmin: n = 3 table over 9138
    # protocols equals the closed form on all 834; n = 4 minimal size
    # equals support on all 4992 (reachability at sizes 1 and 2)
    table3, meta3, atoms3, prices3 = protocol_argmin_table(3, e0, 3)
    dom3 = signed_presentations(3, 3)
    argmin_ok = (len(meta3) == 9138 and len(atoms3) == 36
                 and all(table3[mat_key(x)] == fd3_price(x, 3, e0)
                         for x in dom3))
    cost4 = uniform_cost(4, e0)
    atoms4 = cheap_signed_words(4, cost4)
    reach1, reach2 = set(), set()
    supp_le_size_ok = True
    for t in range(len(atoms4)):
        e, w = atoms4[t]
        k1 = mat_key(realize_protocol([(e, w)], 4))
        reach1.add(k1)
        supp_le_size_ok = supp_le_size_ok and supp_size(
            realize_protocol([(e, w)], 4)) <= 1
    for combo in combinations_with_replacement(range(len(atoms4)), 2):
        m = realize_protocol([atoms4[t] for t in combo], 4)
        reach2.add(mat_key(m))
        supp_le_size_ok = supp_le_size_ok and supp_size(m) <= 2
    n4_ok = len(atoms4) == 96
    for x in signed_presentations(4, 3):
        s, key = supp_size(x), mat_key(x)
        if s == 1:
            n4_ok = n4_ok and key in reach1
        elif s == 2:
            n4_ok = n4_ok and key not in reach1 and key in reach2
        else:
            n4_ok = n4_ok and key not in reach2
    legs["protocol_argmin_exhaustive_n3_n4_matches_closed_form"] = (
        argmin_ok and n4_ok and supp_le_size_ok
        # the billing paths tie by value on a stride of the enumeration
        and all(_bill(prices3, combo)
                == protocol_cost([atoms3[t] for t in combo],
                                 uniform_cost(3, e0))
                for _, _, _, combo in meta3[::101]))
    # (e) THE CANCELLATION LEG: every enumerated protocol covering a
    # cell outside the support of its realized element hits each such
    # cell an even number >= 2 of times with sign-sum zero, has size
    # >= |supp| + 2, and is strictly costlier than eps*|supp|
    over_count, canc_ok = 0, True
    for k, c, key, combo in meta3:
        x = [list(r) for r in key]
        s = supp_size(x)
        hits = defaultdict(list)
        for t in combo:
            e, w = atoms3[t]
            hits[word_cell(w)].append(e)
        off = [cell for cell in hits if x[cell[0]][cell[1]] == 0]
        if off:
            over_count += 1
            canc_ok = (canc_ok and k >= s + 2
                       and c >= (s + 2) * e0
                       and c > s * e0
                       and all(len(hits[cell]) >= 2
                               and len(hits[cell]) % 2 == 0
                               and sum(hits[cell]) == 0
                               for cell in off))
    legs["cancellation_overshoot_strictly_costlier"] = (
        canc_ok and over_count > 0)
    # (f) sampled larger cases at n = 5, support 4, incl. diagonal
    larger = [
        (5, [(0, 1, 1), (1, 2, -1), (2, 3, 1), (3, 4, -1)], 4),
        (5, [(0, 1, 1), (0, 2, 1), (0, 3, -1), (0, 4, 1)], 4),
        (5, [(0, 0, 1), (1, 1, -1), (2, 2, 1), (3, 3, -1)], 4),
    ]
    lg_ok = len(larger) == 3
    for n, entries, es in larger:
        x = cellmat(n, entries)
        prot = cell_protocol(x, n)
        lg_ok = (lg_ok and supp_size(x) == es
                 and realize_protocol(prot, n) == x
                 and protocol_cost(prot, uniform_cost(n, e0)) == es * e0
                 and fd3_price(x, n, e0) == es * e0)
    # a cancelling 5-word control at n = 5: support strictly below size
    ctl = [(1, (0, 1)), (1, (1, 2)), (1, (2, 3)), (1, (0, 4)),
           (-1, (0, 4))]
    xc = realize_protocol(ctl, 5)
    legs["sampled_larger_cases_n5"] = (
        lg_ok and supp_size(xc) == 3 and len(ctl) == 5
        and protocol_cost(ctl, uniform_cost(5, e0)) == 5 * e0
        and protocol_cost(ctl, uniform_cost(5, e0))
            > fd3_price(xc, 5, e0))
    # (g) two eps scales, tied by value: the whole n = 3 table scales
    e1 = 3 * e0
    table3b, _, _, _ = protocol_argmin_table(3, e1, 3)
    legs["scaled_eps_argmin_and_closed_form_tied"] = (
        e1 == 3 * e0 and e1 != e0
        and sorted(table3b) == sorted(table3)
        and all(table3b[k] == 3 * table3[k] for k in table3)
        and all(fd3_price(x, 3, e1) == 3 * fd3_price(x, 3, e0)
                for x in dom3[::50]))
    return _result("check_T_fd3_valuation_closed_form", legs, fails,
                   {"protocols_enumerated_n3": len(meta3),
                    "overshooting_protocols_n3": over_count,
                    "exhaustive_presentations": att_counts,
                    "n4_reach_sizes": [len(reach1), len(reach2)]})

# ---------------------------------------------------------------------------
# C2
# ---------------------------------------------------------------------------

def check_T_md_super_derived_with_equality():
    legs, fails = {}, []
    e0 = probed_eps()[0]
    doms = {(n, k): k_set_domain(n, k)
            for n in (3, 4) for k in (2, 3)}
    counts = {key: len(dom) for key, dom in doms.items()}
    legs["signed_k_sets_support_equals_k"] = (
        counts == {(3, 2): 60, (3, 3): 160, (4, 2): 264, (4, 3): 1760}
        and all(supp_size(x) == k
                for (n, k), dom in doms.items() for _, _, x in dom))
    table3, _, _, _ = protocol_argmin_table(3, e0, 3)
    legs["valuation_prices_k_sets_at_k_eps"] = (
        all(fd3_price(x, n, e0) == k * e0
            for (n, k), dom in doms.items() for _, _, x in dom)
        and all(table3[mat_key(x)] == k * e0
                for (n, k), dom in doms.items() if n == 3
                for _, _, x in dom))
    # under COST_REPRESENTATION_ON_LOADS: phi(x^T x) = c(x) = k*eps,
    # and the no-discount inequality holds WITH EQUALITY; the diagonal
    # part Tr(x^T x) = k is verified per instance
    phi_ok = True
    for (n, k), dom in doms.items():
        for _, _, x in dom:
            g = matmul(mt(x, n), x, n)
            v = phi_load(x, n, e0)
            phi_ok = (phi_ok and v == k * e0 and v >= k * e0
                      and trace_of(g, n) == k
                      and e0 * trace_of(g, n) == v)
    legs["cost_representation_phi_equals_k_eps_with_equality"] = phi_ok
    # tie by value to the banked md_super system: same (S, signs)
    # enumeration set-exactly, and every row's constant part equals
    # C1's valuation on that row's own signed set
    tie_ok = True
    for n in (3, 4):
        rows, _ = nodiscount_system(n, e0)
        tie_ok = (tie_ok
                  and {(S, signs) for _, _, S, signs in rows}
                      == {(S, signs) for S, signs, _ in doms[(n, 2)]}
                  and len(rows) == counts[(n, 2)]
                  and all(const
                          == fd3_price(signed_combo(n, S, signs), n, e0)
                          for _, const, S, signs in rows))
    legs["tie_by_value_to_banked_nodiscount_rows"] = tie_ok
    # the premise's weak form, evaluated over its own quantifier
    # domain: zero violations, zero slack, counts pinned
    viol, slack_nonzero, weak_counts = 0, 0, []
    for n in (3, 4):
        dom = doms[(n, 2)]
        weak_counts.append(len(dom))
        for _, _, x in dom:
            v = phi_load(x, n, e0)
            if v < 2 * e0:
                viol += 1
            if v - 2 * e0 != 0:
                slack_nonzero += 1
    legs["derived_weak_form_zero_violations_zero_slack"] = (
        weak_counts == [60, 264] and viol == 0 and slack_nonzero == 0)
    # two scales, tied by value
    e1 = 3 * e0
    legs["scaled_eps_two_scales_tied"] = (
        e1 == 3 * e0 and e1 != e0
        and all(phi_load(x, n, e1) == 3 * phi_load(x, n, e0)
                and phi_load(x, n, e1) == k * e1
                for (n, k), dom in doms.items()
                for _, _, x in dom[::7]))
    return _result("check_T_md_super_derived_with_equality", legs, fails,
                   {"instance_counts": {f"n{n}_k{k}": c
                                        for (n, k), c in counts.items()},
                    "weak_form_violations": viol,
                    "weak_form_slack_nonzero": slack_nonzero,
                    "derivation_step":
                        "phi_load := fd3_price -- COST_REPRESENTATION_ON_"
                        "LOADS, a definitional identification, consumed "
                        "and not derived. The legs "
                        "cost_representation_phi_equals_k_eps_with_"
                        "equality and derived_weak_form_zero_violations_"
                        "zero_slack restate C1's closed form through that "
                        "identification; the computed content outside it "
                        "is the closed form itself and the set-exact "
                        "value tie to the banked md_super rows. The "
                        "registry key T_md_super_derived_with_equality is "
                        "not qualified; this field is."})

# ---------------------------------------------------------------------------
# C3
# ---------------------------------------------------------------------------

def check_T_center_forced_born_pricing():
    legs, fails = {}, []
    e0 = probed_eps()[0]
    systems = {}
    for n in (3, 4):
        coeff, consts, rhs, unk = equality_system(n, e0, (2, 3))
        coeff2, _, _, _ = equality_system(n, e0, (2,))
        nz = [r for r in coeff if any(c != 0 for c in r)]
        nz2 = [r for r in coeff2 if any(c != 0 for c in r)]
        systems[n] = (coeff, consts, rhs, unk, nz, nz2)
    # negative-pivot controls on the local elimination path: rank must
    # be found through negative entries too (the equality systems here
    # happen to offer a positive pivot at every visited column, so
    # these fixtures carry the discriminating content)
    neg_controls = (
        gauss_rank([[F(-1)]]) == 1 == matrix_rank([[F(-1)]])
        and gauss_rank([[F(0), F(-3)], [F(0), F(-3)]]) == 1
        and matrix_rank([[F(0), F(-3)], [F(0), F(-3)]]) == 1
        and gauss_rank([[F(-2), F(0)], [F(0), F(-2)]]) == 2)
    legs["equality_system_kernel_zero_independent_gauss"] = (
        neg_controls and all(
            gauss_rank(nz) == len(unk) == gauss_rank(nz2)
            and gauss_rank(nz) == matrix_rank(nz)
            and len(nz) > 0 and len(nz2) > 0
            for n, (coeff, consts, rhs, unk, nz, nz2)
            in systems.items()))
    # the inhomogeneity vanishes BECAUSE the rhs is the valuation:
    # const = eps*Tr(x^T x) = c(x) = rhs, per row, both sizes -- the
    # k-resolution equality is the valuation's output, and the
    # equality-as-premise name sits in NOT_CONSUMED.  The expected rhs
    # is rebuilt independently at this leg site from the domain's own
    # k*eps, and the rhs-from-the-valuation tie is by value: a decoy
    # price function fed through the price_fn hook moves the system's
    # rhs by exactly its offset while the consts do not move
    expected_rhs = {n: [k * e0 for k in (2, 3)
                        for _ in k_set_domain(n, k)]
                    for n in (3, 4)}
    decoy_ok = True
    for n in (3, 4):
        _, consts_d, rhs_d, _ = equality_system(
            n, e0, (2, 3),
            price_fn=lambda x, n_, e_: fd3_price(x, n_, e_) + e_)
        decoy_ok = (decoy_ok
                    and rhs_d == [v + e0 for v in expected_rhs[n]]
                    and consts_d == systems[n][1]
                    and rhs_d != systems[n][2])
    legs["equality_rhs_is_valuation_output_not_premise"] = (
        all(consts == rhs and rhs == expected_rhs[n]
            and len(consts) == len(coeff) > 0
            for n, (coeff, consts, rhs, unk, nz, nz2)
            in systems.items())
        and decoy_ok
        and "MISSING_LEMMA_EQUALITY_AS_PREMISE" in PREMISES_NOT_CONSUMED)
    # the sibling's axis-pair deduction, cross-checked by value: the
    # forced solution covers every unknown and forces zero -- the same
    # solution the kernel-zero homogeneous system has
    sib_ok = True
    for n in (3, 4):
        rows, unk_sib = nodiscount_system(n, e0)
        axis_pairs, forced = forced_solution(rows, unk_sib, e0)
        want = {(u, v) for u in range(len(unk_sib))
                for v in (F(2), F(-2))}
        sib_ok = (sib_ok and axis_pairs == want
                  and sorted(forced) == sorted(unk_sib)
                  and all(v == F(0) for v in forced.values())
                  and sorted(unk_sib) == sorted(systems[n][3]))
        # the symmetrization-factor convention, tied by value across
        # modules: equality_system's own coeff rows for the
        # ((0,1),(0,2))/(1,+-1) sets equal the sibling's
        # nodiscount_system coeff tuples for the same (S, signs) --
        # the coefficient VALUES are tied, entrywise.  The SPELLING is
        # not: g is symmetric, so g_ij + g_ji and 2*g_ij are the same
        # value and this tie cannot separate them.
        sib_by_key = {(S, signs): dict(zip(unk_sib, cf))
                      for cf, _, S, signs in rows}
        unk_here = systems[n][3]
        tied = 0
        for idx, (S, signs, x) in enumerate(k_set_domain(n, 2)):
            if S == ((0, 1), (0, 2)) and signs in ((1, 1), (1, -1)):
                tied += 1
                sib_ok = (sib_ok
                          and dict(zip(unk_here, systems[n][0][idx]))
                              == sib_by_key[(S, signs)])
        sib_ok = sib_ok and tied == 2
    legs["sibling_forced_solution_value_tie"] = sib_ok
    # at the solution W = eps*I the functional is eps*Tr on every
    # sample element, with a non-forced-off-diagonal control that
    # disagrees on at least one
    n = 3
    W0 = sym_from_offdiag(n, e0, {})
    b = [[F(1), F(2), F(0)], [F(0), F(1), F(-1)], [F(3), F(0), F(1)]]
    esym = [[F(2), F(1), F(0)], [F(1), F(2), F(1)], [F(0), F(1), F(2)]]
    sand = matmul(matmul(mt(b, n), esym, n), b, n)
    samples = ([matmul(mt(x, n), x, n)
                for _, _, x in k_set_domain(3, 2)[::11]]
               + [esym, sand, unit_matrix(3, 1, 1)])
    tvals = [trace_of(M, n) for M in samples]
    W_bad = sym_from_offdiag(n, e0, {(1, 2): e0 / 2})
    legs["center_functional_is_eps_trace_with_control"] = (
        len(samples) == 9
        and all(phi_of(W0, M, n) == e0 * t
                for M, t in zip(samples, tvals))
        and len({str(t) for t in tvals}) > 1
        and any(phi_of(W_bad, M, n) != e0 * t
                for M, t in zip(samples, tvals)))
    # every off-diagonal perturbation breaks the equality somewhere
    pert_ok, pert_n = True, 0
    dom32 = k_set_domain(3, 2)
    for u in [(0, 1), (0, 2), (1, 2)]:
        for d in (e0, -e0, e0 / 2, -e0 / 2):
            Wp = sym_from_offdiag(3, e0, {u: d})
            resid = [phi_of(Wp, matmul(mt(x, 3), x, 3), 3) - 2 * e0
                     for _, _, x in dom32]
            pert_n += 1
            pert_ok = pert_ok and any(r != 0 for r in resid)
    legs["offdiagonal_perturbation_breaks_equality"] = (
        pert_ok and pert_n == 12)
    # scaled eps: the forced center scales, the trace values scale
    e1 = 3 * e0
    coeff_s, consts_s, rhs_s, unk_s = equality_system(3, e1, (2, 3))
    nz_s = [r for r in coeff_s if any(c != 0 for c in r)]
    W0s = sym_from_offdiag(3, e1, {})
    legs["scaled_eps_center_scales"] = (
        e1 == 3 * e0 and e1 != e0
        and consts_s == rhs_s and gauss_rank(nz_s) == len(unk_s)
        and all(phi_of(W0s, M, 3) == 3 * phi_of(W0, M, 3)
                for M in samples))
    return _result("check_T_center_forced_born_pricing", legs, fails,
                   {"system_rows": {str(n): len(systems[n][0])
                                    for n in (3, 4)},
                    "unknowns": {str(n): len(systems[n][3])
                                 for n in (3, 4)},
                    "perturbations_tested": pert_n})

# ---------------------------------------------------------------------------
# C4
# ---------------------------------------------------------------------------

def check_L_rank_model_excluded_no_superposed_image():
    legs, fails = {}, []
    e0 = probed_eps()[0]
    with open(_witness.__file__, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    legs["witness_module_sha_pinned"] = (digest == WITNESS_SHA256)
    # the computed witness: the rank model prices E_01 +- E_02 at eps;
    # the protocol infimum (exhaustive C1 table) is 2*eps
    table3, _, _, _ = protocol_argmin_table(3, e0, 3)
    wit_ok = True
    for sgn in (1, -1):
        x = signed_combo(3, ((0, 1), (0, 2)), (1, sgn))
        wit_ok = (wit_ok
                  and rank_price(x, 3, e0) == e0
                  and rank_price(x, 3, e0) == e0 * matrix_rank(x)
                  and matrix_rank(x) == 1 == rank_by_minors(x)
                  and table3[mat_key(x)] == 2 * e0
                  and rank_price(x, 3, e0) < table3[mat_key(x)])
    legs["rank_model_disagrees_with_protocol_infimum"] = wit_ok
    # no protocol infimum below k*eps on any signed k-set: exhaustive
    # table at n = 3 (k = 2, 3), reachability at n = 4 (k = 2)
    low_ok, low_counts = True, []
    for k in (2, 3):
        dom = k_set_domain(3, k)
        low_counts.append(len(dom))
        low_ok = low_ok and all(table3[mat_key(x)] == k * e0
                                for _, _, x in dom)
    cost4 = uniform_cost(4, e0)
    atoms4 = cheap_signed_words(4, cost4)
    reach1 = {mat_key(realize_protocol([a], 4)) for a in atoms4}
    dom42 = k_set_domain(4, 2)
    low_counts.append(len(dom42))
    low_ok = low_ok and all(mat_key(x) not in reach1
                            for _, _, x in dom42)
    legs["no_protocol_prices_signed_k_set_below_k_eps"] = (
        low_ok and low_counts == [60, 160, 264]
        # nonemptiness pin on the negative-membership half (audit 3
        # MINOR-1): reach1 is the full size-1 reachable set, 32 keys
        # as C1's key_result reports
        and len(reach1) == 32)
    # the word image contains no superposed element: at n = 3 and 4 it
    # is exactly the set of matrix units, every element support one
    img_ok, img_sizes = True, []
    supers = {}
    for n in (3, 4):
        ws = words_on(uniform_cost(n, e0), 6)
        image = {mat_key(realize_protocol([(1, w)], n)) for w in ws}
        img_sizes.append(len(image))
        units = {mat_key(unit_matrix(n, i, j))
                 for i in range(n) for j in range(n)}
        sup_plus = mat_key(signed_combo(n, ((0, 1), (0, 2)), (1, 1)))
        sup_minus = mat_key(signed_combo(n, ((0, 1), (0, 2)), (1, -1)))
        supers[n] = (sup_plus, sup_minus)
        img_ok = (img_ok and image == units and len(image) == n * n
                  # the word enumeration size, pinned as at C1
                  and len(ws) == {3: 378, 4: 4368}[n]
                  # the +- witness pair is two distinct elements
                  and sup_plus != sup_minus
                  and sup_plus not in image and sup_minus not in image
                  and all(supp_size([list(r) for r in key]) == 1
                          for key in image))
    legs["word_image_no_superposed_element"] = (
        img_ok and img_sizes == [9, 16])
    # the permissive pole's atom is rank one yet outside the image:
    # a superposed rank-one atom no substrate operation contracts to
    atom_ok = True
    strict_fiber_empty = True
    for n in (3, 4):
        ws = words_on(uniform_cost(n, e0), 6)
        image = {mat_key(realize_protocol([(e, w)], n))
                 for w in ws for e in (1, -1)}
        # the word enumeration size, pinned as at C1
        atom_ok = atom_ok and len(ws) == {3: 378, 4: 4368}[n]
        # the signed single-word image is the full signed unit set
        # (nonemptiness pinned by value) and excludes the witness pair
        strict_fiber_empty = (strict_fiber_empty
                              and len(image) == 2 * n * n
                              and all(key not in image
                                      for key in supers[n]))
        for key in supers[n]:
            m = [list(r) for r in key]
            atom_ok = (atom_ok and matrix_rank(m) == 1
                       and rank_by_minors(m) == 1
                       and key not in image)
    legs["rank_atom_not_substrate_contractible"] = atom_ok
    # the strict pole, computed (audit 3 MINOR-4): the superposed
    # witness pair has an EMPTY signed single-word fiber (outside the
    # signed word image, whose size is pinned) while the adopted
    # valuation prices each at the finite protocol infimum 2*eps from
    # the exhaustive C1 table -- the strict pole's unpriceable verdict
    # and the computed table disagree on a named instance
    legs["strict_pole_empty_signed_word_fiber_yet_protocol_priced"] = (
        strict_fiber_empty
        and len(supers[3]) == 2
        and all(table3[key] == 2 * e0 for key in supers[3]))
    return _result("check_L_rank_model_excluded_no_superposed_image",
                   legs, fails,
                   {"word_image_sizes": img_sizes,
                    "exclusion_witness": "c_rank(E_01+E_02) = eps < "
                                         "2*eps = protocol infimum",
                    "witness_sha256": digest[:16] + "..."})

# ---------------------------------------------------------------------------
# C5
# ---------------------------------------------------------------------------

def check_L_residual_ledger_retirement():
    legs, fails = {}, []
    legs["consumed_set_exact"] = (
        sorted(PREMISES_CONSUMED) == [
            "A2_ARGMIN", "CARRIER_COMPLETENESS",
            "COST_REPRESENTATION_ON_LOADS", "DEF_APS_STRUCTURE_COST",
            "DEF_REALIZATION_SIGNED_CONTRACTION",
            "EQUAL_COST_UNIFORMITY", "FD3_FLOOR",
            "FD3_VALUATION_CONVENTION", "FD4_FINITE_CARRIER",
            "LINEAR_REALIZATION_TARGET",
            "NONEMPTY_ENFORCEMENT_PRESENTATION",
            "REAL_SYMMETRIC_TEST_SECTOR",
        ]
        and frozenset(WORD_PREMISES_CONSUMED) < PREMISES_CONSUMED
        and frozenset(ELL_PREMISES_CONSUMED) < PREMISES_CONSUMED
        and "REAL_SYMMETRIC_TEST_SECTOR" in ELL_PREMISES_CONSUMED
        and frozenset(NAMED_CLAUSES) < PREMISES_CONSUMED)
    legs["not_consumed_set_exact_with_derived_here_marker"] = (
        sorted(PREMISES_NOT_CONSUMED) == [
            "CYCLICITY", "DIVISION_RING_SELECTION",
            "MD_SUPER_NODISCOUNT",
            "MISSING_LEMMA_EQUALITY_AS_PREMISE",
            "P1_SANDWICH_REALIZATION", "P2_PRESENTATION_GAUGE",
            "P3_UNDERIVED", "PHI_EQ_EPS_TR_STIPULATION",
        ]
        and DERIVED_HERE == frozenset({"MD_SUPER_NODISCOUNT"})
        and DERIVED_HERE < PREMISES_NOT_CONSUMED
        and not (DERIVED_HERE & PREMISES_CONSUMED)
        and NOT_TOUCHED < PREMISES_NOT_CONSUMED
        and sorted(NOT_TOUCHED) == [
            "CYCLICITY", "DIVISION_RING_SELECTION",
            "P1_SANDWICH_REALIZATION", "P2_PRESENTATION_GAUGE",
            "P3_UNDERIVED",
        ])
    # the retired name, cross-checked against the trio: the md_super
    # sibling consumes MD_SUPER_NODISCOUNT as its named residual and
    # every one of its records carries it in conditional_on; here the
    # same name is derived output, consumed nowhere
    md_rec = _md_premise_check()
    legs["retired_name_cross_checked_against_trio"] = (
        MD_RESIDUAL_PREMISES == DERIVED_HERE
        and MD_RESIDUAL_PREMISES <= MD_PREMISES_CONSUMED
        and md_rec["passed"] is True
        and md_rec["conditional_on"] == sorted(DERIVED_HERE)
        and "MD_SUPER_NODISCOUNT" not in PREMISES_CONSUMED
        and "MD_SUPER_NODISCOUNT" not in CONDITIONAL_ON)
    legs["conditional_on_carries_four_clauses"] = (
        CONDITIONAL_ON == [
            "COST_REPRESENTATION_ON_LOADS",
            "DEF_REALIZATION_SIGNED_CONTRACTION",
            "FD3_VALUATION_CONVENTION",
            "LINEAR_REALIZATION_TARGET",
        ]
        and set(CONDITIONAL_ON)
            == frozenset(NAMED_CLAUSES)
               | frozenset({"FD3_VALUATION_CONVENTION",
                            "LINEAR_REALIZATION_TARGET"})
        and sorted(NAMED_CLAUSES) == [
            "COST_REPRESENTATION_ON_LOADS",
            "DEF_REALIZATION_SIGNED_CONTRACTION",
        ]
        and sorted(EXCLUDED_ALTERNATIVES) == ["permissive_pole",
                                              "strict_pole"]
        and all(isinstance(v, str) and len(v) > 0
                for v in NAMED_CLAUSES.values()))
    legs["consumed_disjoint_from_not_consumed"] = (
        not (PREMISES_CONSUMED & PREMISES_NOT_CONSUMED)
        and len(PREMISES_CONSUMED) == 12
        and len(PREMISES_NOT_CONSUMED) == 8)
    legs["linearity_residual_carried_not_discharged"] = (
        "LINEAR_REALIZATION_TARGET" in PREMISES_CONSUMED
        and "LINEAR_REALIZATION_TARGET" in CONDITIONAL_ON
        and "LINEAR_REALIZATION_TARGET" in WORD_PREMISES_CONSUMED
        and "LINEAR_REALIZATION_TARGET" not in DERIVED_HERE)
    # a fresh own-emitted record, read back (audit 3 MAJOR-1): its
    # conditional_on equals, by value, the four named premises and the
    # module-level CONDITIONAL_ON data
    own_rec = check_L_scope_fences()
    legs["own_emitted_record_carries_conditional_on"] = (
        own_rec["conditional_on"] == [
            "COST_REPRESENTATION_ON_LOADS",
            "DEF_REALIZATION_SIGNED_CONTRACTION",
            "FD3_VALUATION_CONVENTION",
            "LINEAR_REALIZATION_TARGET",
        ]
        and own_rec["conditional_on"] == list(CONDITIONAL_ON))
    return _result("check_L_residual_ledger_retirement", legs, fails,
                   {"consumed": len(PREMISES_CONSUMED),
                    "not_consumed": len(PREMISES_NOT_CONSUMED),
                    "derived_here": sorted(DERIVED_HERE),
                    "conditional_on": list(CONDITIONAL_ON),
                    "what_this_check_establishes":
                        "Five legs -- consumed_set_exact, "
                        "not_consumed_set_exact_with_derived_here_marker, "
                        "conditional_on_carries_four_clauses, "
                        "consumed_disjoint_from_not_consumed, "
                        "linearity_residual_carried_not_discharged -- "
                        "read name lists declared in this file and "
                        "literal copies of them written in the same file. "
                        "PREMISES_CONSUMED, read by consumed_set_exact, "
                        "not_consumed_set_exact_with_derived_here_marker, "
                        "consumed_disjoint_from_not_consumed and "
                        "linearity_residual_carried_not_discharged, is "
                        "built from the premise sets imported from "
                        "word_carrier_transfer and carrier_elliptope; "
                        "consumed_set_exact reads both of those imported "
                        "sets directly and "
                        "linearity_residual_carried_not_discharged reads "
                        "the word_carrier_transfer one. None establishes "
                        "what a name denotes, and a rename carried on "
                        "every copy is invisible to them. Two legs "
                        "execute a check and read its emitted record back "
                        "by value: retired_name_cross_checked_against_trio "
                        "executes the md_super sibling's check and reads "
                        "its conditional_on, and "
                        "own_emitted_record_carries_conditional_on emits a "
                        "fresh record here and reads its conditional_on."})

# ---------------------------------------------------------------------------
# C6
# ---------------------------------------------------------------------------

def check_L_scope_fences():
    legs, fails = {}, []
    e0 = probed_eps()[0]
    # the fence's computed reason: off the complete carrier the banked
    # psi_min prices by word distance and the closed form does not
    p3 = {frozenset((0, 1)): e0, frozenset((1, 2)): e0}
    vals_p3, _ = argmin_values(p3, 6, "set", closed_only=False)
    u02 = unit_matrix(3, 0, 2)
    legs["p3_divergence_fence_reason"] = (
        vals_p3[(0, 2)] == 2 * e0
        and fd3_price(u02, 3, e0) == e0
        and fd3_price(u02, 3, e0) != vals_p3[(0, 2)])
    # control: on the complete uniform carrier the valuation agrees
    # with psi_min on every unit
    vals_c, _ = argmin_values(uniform_cost(3, e0), 6, "set",
                              closed_only=False)
    legs["complete_uniform_carrier_control"] = all(
        vals_c[(i, j)] == e0
        and fd3_price(unit_matrix(3, i, j), 3, e0) == vals_c[(i, j)]
        for i in range(3) for j in range(3))
    # the signed-unit-coefficient domain, entry by entry
    checked = 0
    signed_ok = True
    for n in (3, 4):
        for x in signed_presentations(n, 3):
            checked += 1
            signed_ok = signed_ok and all(
                v in (F(1), F(-1), F(0)) for row in x for v in row)
    for n, k in ((3, 2), (3, 3), (4, 2), (4, 3)):
        for _, _, x in k_set_domain(n, k):
            checked += 1
            signed_ok = signed_ok and all(
                v in (F(1), F(-1), F(0)) for row in x for v in row)
    legs["signed_unit_coefficient_domain"] = (
        signed_ok and checked == 834 + 4992 + 60 + 160 + 264 + 1760)
    # the symmetric slice: every load x^T x is symmetric and every
    # antisymmetric coefficient matrix scores zero on it (nonzero
    # control on a non-symmetric element)
    A = [[F(0), F(3), F(-1)], [F(-3), F(0), F(2)], [F(1), F(-2), F(0)]]
    sym_ok, inert_n = True, 0
    for _, _, x in k_set_domain(3, 2):
        g = matmul(mt(x, 3), x, 3)
        inert_n += 1
        sym_ok = (sym_ok and g == mt(g, 3)
                  and phi_of(A, g, 3) == F(0))
    legs["symmetric_slice_antisymmetric_inert"] = (
        sym_ok and inert_n == 60
        and A == [[-A[j][i] for j in range(3)] for i in range(3)]
        and phi_of(A, unit_matrix(3, 0, 1), 3) == F(3)
        and phi_of(A, unit_matrix(3, 0, 1), 3) != 0)
    return _result("check_L_scope_fences", legs, fails,
                   {"p3_psi_min_E02": str(vals_p3[(0, 2)]),
                    "closed_form_E02": str(fd3_price(u02, 3, e0)),
                    "signed_entries_checked": checked})

# ---------------------------------------------------------------------------

ALL_CHECKS = [
    check_T_fd3_valuation_closed_form,
    check_T_md_super_derived_with_equality,
    check_T_center_forced_born_pricing,
    check_L_rank_model_excluded_no_superposed_image,
    check_L_residual_ledger_retirement,
    check_L_scope_fences,
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
    'T_fd3_valuation_closed_form': check_T_fd3_valuation_closed_form,
    'T_md_super_derived_with_equality':
        check_T_md_super_derived_with_equality,
    'T_center_forced_born_pricing': check_T_center_forced_born_pricing,
    'L_rank_model_excluded_no_superposed_image':
        check_L_rank_model_excluded_no_superposed_image,
    'L_residual_ledger_retirement': check_L_residual_ledger_retirement,
    'L_scope_fences': check_L_scope_fences,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


if __name__ == "__main__":
    run_all()
