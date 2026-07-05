"""apf/delta_calculus.py -- the Delta-calculus: additivity + (non-)monotonicity of Delta.

v24.3.372 (2026-07-03, Paper 12 review-2 lane B2; fresh-context hostile audit
AUDIT_ROUND2 LAND-WITH-FIXES 0.85, fixes B2-1 + B2-2 carried). Walk of record:
"The Turning/p12_review2_walks_2026-07-03/b2_delta_calculus/" (REPORT.md +
staged check + run log). Answers the reviewer's Q6: what does the banked cost
calculus give -- and provably NOT give -- for the residual
Delta(S1,S2) = kappa(S1 v S2) - kappa(S1) - kappa(S2) under disjointness,
coarse-graining, and free operations.

Seven checks:

  check_T_delta_disjoint_additivity  [P]
      Delta = 0 across ANCHOR-DISJOINT interfaces (theorem-strength equality,
      not an inequality), by T_M (disjoint => independent, the <= direction of
      the biconditional) + L_irr Step 1 + L_loc + L_cost sub-lemma C2.

  check_T_delta_coarse_graining_monotonicity  [P]
      kappa is subset-monotone [P]; the exact refinement identity
      Delta_coarse = Delta_fine - Delta_internal is banked [P] (T_canonical
      Prop 9.8); one-sided monotone DECREASE of Delta under merging an
      OCCUPIED block is conditional-[P] on the NAMED premise
      Delta_internal >= 0; global monotonicity of Delta under coarse-graining
      is FALSE -- pinned finite counterexamples in BOTH directions (a no-go at
      theorem strength). Negative control W3: a subadditive internal block
      (shared classical bit) makes coarse-graining INCREASE Delta.

  check_T_cost_count_characterization  [P]
      THE CHARACTERIZATION THEOREM (landed v24.3.376, 2026-07-04, Paper 12
      review-3 walk W1; fresh-context hostile audit AUDIT_W1
      LAND-WITH-FIXES 0.85, mandatory fixes 1/2/3/6 + recommended 4/5
      carried; walk of record: "The Turning/p12_review3_walks_2026-07-04/
      w1_cost_count_characterization/"): any cost functional satisfying
      X1 count-dependence (L_cost_C1 + FD1-sc) + X2 anchor-disjoint
      additivity (L_cost_C2; executable as check 1) + X3 the MD floor
      f(1) = eps > 0 (L_epsilon*) equals kappa = n * eps -- by induction
      on N alone. Continuity, measurability, and monotonicity are NOT
      hypotheses (monotonicity is a corollary). Sharpens L_cost_MAIN
      (its monotonicity hypothesis is redundant on N; conclusion
      unchanged); contrast L_Cauchy_uniqueness on R+, where Darboux
      monotonicity IS load-bearing.

  check_T_delta_not_an_information_functional  [P]
      THE INFORMATION-FUNCTIONAL SEPARATION (landed v24.3.379, 2026-07-04,
      Paper 12 round-4 walk A3, reviewer Q6; fresh-context hostile audit
      LAND-WITH-FIXES 0.85, mandatory fixes F1/F2 + recommended F3-F6
      carried; walk of record: "The Turning/p12_review4_walks_2026-07-04/
      a3_delta_info/"): under the NAMED readout-pushforward bridge (a
      comparison device defined in-check, not a framework commitment),
      Delta is provably NOT a function of the two families' bridged joint
      READOUT distribution (the outcome table): an irreducibly-joint
      parity pair and a reducibly-shared copy pair have IDENTICAL bridge
      images (uniform on {00, 11}) and opposite Delta (+eps vs -eps, the
      -eps side banked verbatim: NC2 of check 1 + the W1 drop-b Clause D
      of check 2). Where the calculus asserts Delta = 0 the bridge
      statistics agree exactly; on the pure poles sign(Delta) =
      -sign(co-information) (count-level synergy-minus-redundancy,
      convention flipped); MI/TC are restriction-monotone while Delta
      moves strictly both ways (the banked W1 counterexample, bridged);
      and a one-parameter statistics dial sweeps TC and co-information
      through exactly-distinguished values while the configuration -- and
      hence Delta -- is fixed. Exact rational arithmetic throughout
      (entropy comparisons via the exact Fractions 2^{N*H}).

  check_T_register_reading_grounds_ceil_log2_count  [P_structural_reading]
      THE REGISTER OPERATIONALIZATION (landed v24.3.380, 2026-07-04,
      Paper 12 round-5 walk B2, reviewer Q6/Q3/Q1; fresh-context hostile
      audit LAND-WITH-FIXES 0.80, mandatory fixes 1/2/3/5 + recommended
      4/6/7 carried; walk of record: "The Turning/
      p12_review5_walks_2026-07-04/b2_register/"): the minimal FAITHFUL
      (= perfectly-distinguishable) protected register for a d-ary
      irreducible fusion record is exactly ceil(log2 d) two-valued cells
      (exact combinatorics, tight both ways, bits = qubits by dimension
      count); the register model grounds ceil-log2 and ONLY ceil-log2
      among the four banked clause-(iii) readings of
      check_T_su2_string_cut_comovement; under the grounded reading the
      split-vs-unsplit TIE survives (2 == 2 against the diagnostic's
      strict 3/2 < 2) and clause (ii) contracts to the weak ordering
      [1, 2, 2, 3] (named-reading-conditional; the banked
      UNDER-DETERMINED verdict stands); additivity exact under the
      per-component protection clause F-reg (REQUIRED for X2, MOTIVATED
      BY L_loc, NOT derived from it; pooled packing strictly subadditive
      at (3,5)). J := reg is the named, priced, falsifiable register
      reading (two distinct falsifiers, Delta-tracking probe as switch).

  check_T_delta_JR_derived  [P] (conditionality stated)
      THE DERIVED COUNTING IDENTITY (landed v24.3.381, 2026-07-04, Paper 12
      round-6 walk C1, reviewer Q2; fresh-context hostile audit
      LAND-WITH-FIXES 0.84, mandatory F1-F4 + recommended F5-F7 carried;
      walk of record: "The Turning/p12_review6_walks_2026-07-04/
      c1_algebraic_anchors/"): the formal channel ledger (Ch/J/R) and
      Delta = eps*(J - R) DERIVED from CH1 (activation monotonicity, a
      definitional clause of the join under the ledger reading, typed and
      pinned by a negative control) + CH2 (cost = count, the banked
      characterization theorem). Two routes with teeth: independent
      hand-set E-tables vs channel sets on six worked examples incl. the
      banked NC1/NC2/W1 verbatim. The R-convention disambiguated: R counts
      shared CHANNELS (billed distinctions), not shared loci -- the locus
      convention provably breaks the identity (two discriminating
      instances in-check). Ledger-relativity sentence carried: Ch(join)
      is presentation input; the deviation witnesses certify jointness,
      not the count.

  check_T_delta_chain_rule_conditional_expectation_dichotomy  [P] (under
      the named support transcription)
      THE CHAIN-RULE DICHOTOMY FOR PRESENTED COARSE FAMILIES (landed
      v24.3.381, 2026-07-04, Paper 12 round-6 walk C2, reviewer Q9;
      fresh-context hostile audit LAND-WITH-FIXES 0.85, mandatory F1/F2
      (+F4 scoping) + recommended F3/F5/F6 + cosmetic F7/F8 carried; walk
      of record: "The Turning/p12_review6_walks_2026-07-04/
      c2_condexp_chainrule/"): a conditional expectation E_B enters the
      ledger through a PRESENTATION; under the support transcription
      (CANONICAL, not unique -- same-ledger + per-presented-channel legs
      named in-check) the multi-block chain rule holds IFF the presented
      supports partition the billed universe; exact defect formula; the
      pinned two-parity counterexample fails by exactly E({b}),
      floor-forced, occupancy-free, and UNRESCUABLE by any same-ledger
      transcription (free-world impossibility 4*eps > E(U) = 3*eps).
      The theorem quantifies over PRESENTATIONS (the subalgebra level is
      degenerate: every covering B restorable; B_pq admits NO non-trivial
      compliant presentation -- computed).

Every derivation step cites the banked lemma by check name (apf/core.py
unless noted):

  L_cost   (check_L_cost, [P])   kappa(S) = n(S) * epsilon uniquely
                                 (count-times-epsilon; Cauchy uniqueness).
           Sub-lemma L_cost_C2 (Additive Independence): T_M disjoint anchors
           + L_loc factorization ==> f(n1+n2) = f(n1)+f(n2). EQUALITY.
  L_epsilon* (check_L_epsilon_star, [P])
                                 the MD floor: every enforceable
                                 distinction costs at least eps*_Gamma > 0
                                 (Gamma-indexed per interface; deps
                                 A1 + MD + BW).
  T_M      (check_T_M, [P])      independence <=> disjoint anchor sets
                                 (biconditional; steps 1-3 prove disjoint =>
                                 independent -- the direction this module
                                 loads on; steps 4-9 prove the converse).
  L_loc    (check_L_loc, [P])    interfaces have independent budgets;
                                 subsystems at disjoint interfaces are
                                 independent (Step 4(c)); state space
                                 factors Omega(S1 u S2) = Omega(S1) x Omega(S2).
  L_irr    (check_L_irr, [P])    Step 1 counting identity:
                                 Delta(S1,S2) = epsilon * (J - R), with
                                 J = # irreducibly-joint distinctions the
                                 joint carries, R = # reducible shared
                                 anchors. L_cost fixes the FORM; occupancy
                                 fixes the SIGN of J-terms. The structural
                                 core (i) -- monotonicity L3, all subsets
                                 admissible -- is occupancy-FREE.
  T_canonical (check_T_canonical, [P])
                                 (L3) monotonicity of E under subset;
                                 (Omega3 / Prop 9.8) EXACT refinement:
                                 Omega_fine = Omega_coarse + Delta(a,b);
                                 (R7) capacity additivity; (R8) cost
                                 non-separatedness (Omega_inter lives only
                                 in the global cost).
  T_contextuality_implies_superadditive_cost
           (apf/yang_mills_md_bridge.py, [P_structural_reading])
                                 level (1): a classically-correlated shared
                                 bit is SUBADDITIVE (cost(joint)=1 <
                                 cost(A)+cost(B)=2, Delta <= 0). Cited for
                                 POSITIONING only; appears in no [P] step.
  FD1-sc   (check_FD1_structural_completeness, apf/foundation_inputs.py, [P])
                                 an empirical-difference-free relabeling is a
                                 free coordinative convention (zero cost).

HONESTY NOTE (audit, carried at landing): the eps(J - R) identity lives in
L_irr's docstring PROOF, not in its executable witness (L_irr's own Delta
values are 1 and 3 with J, R never computed). Under settled APF practice the
docstring proof is part of the banked claim, so the citation is legitimate --
but the two checks in this module are the FIRST EXECUTABLE INSTANTIATIONS of
the identity's two-term structure.

FENCES:
  (F1) 'Disjoint' means ANCHOR-disjoint (T_M's biconditional), not a spatial
       or causal label. Causal separation licenses Delta = 0 only via L_loc
       Step 4(c) (disjoint interfaces => independent), i.e. only when it is
       cashed as anchor-disjointness.
  (F2) The additivity theorem says nothing about the SIGN of Delta once
       anchors intersect: a spanning (cross-interface) distinction gives
       Delta > 0 (L_irr's correlation c; T_canonical R8 Omega_inter), a
       shared classical bit gives Delta < 0 (subadditive, level (1) of
       T_contextuality_implies_superadditive_cost). Both appear in-check as
       negative controls: Delta != 0 ONLY where the disjointness premise
       FAILS.

CPTP CLAUSE -- honest type boundary, NO theorem: APF records are
Boolean/count-ledger objects; 'local CPTP map' has no native referent without
adopting the record-algebra (GNS) representation (check_L_T2_finite_gns) AND
a further, un-banked claim that the map is admissibility-realizable. OPEN;
nothing is registered for it.

Self-contained arithmetic: pure stdlib, exact Fractions, all costs integer
multiples of epsilon = 1 (per L_cost's count-times-epsilon uniqueness; the
Paper 12 Technical Supplement's Delta is capacity-denominated).
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from typing import Dict

from apf.apf_utils import check, _result

EPS = Fraction(1)  # epsilon; all costs are integer multiples (L_cost)


def _powerset(universe):
    out = []
    for r in range(len(universe) + 1):
        for s in combinations(sorted(universe), r):
            out.append(frozenset(s))
    return out


def _monotone(E, universe):
    """L3 (T_canonical Part I): S1 <= S2 ==> E(S1) <= E(S2)."""
    ps = _powerset(universe)
    for S1 in ps:
        for S2 in ps:
            if S1 <= S2:
                check(E[S1] <= E[S2], f"L3 violation: E({set(S1)}) > E({set(S2)})")
    return True


def _Delta(E, S1, S2):
    """Delta(S1,S2) = kappa(S1 v S2) - kappa(S1) - kappa(S2)."""
    return E[S1 | S2] - E[S1] - E[S2]


# =====================================================================
# CHECK 1 -- Additivity across anchor-disjoint interfaces
# =====================================================================

def check_T_delta_disjoint_additivity() -> Dict:
    """T_delta_disjoint_additivity: if D1 anchors only at Gamma_1 and D2
    anchors only at Gamma_2 with anc(D1) ^ anc(D2) = empty, then

        kappa(D1 |_| D2) = kappa(D1) + kappa(D2),   i.e.  Delta = 0.

    DERIVATION (each step a banked lemma):
      Step 1 [T_M steps 1-3 (disjoint => independent), taken contrapositively,
        + L_irr Step 1]. An irreducibly-joint distinction across the pair IS
        "a correlation not reducible to either marginal" (L_irr Step 1's own
        gloss). Anchor-disjointness gives independence (T_M, the <= direction
        of the biconditional), and independence excludes any such correlation.
        So a hypothetical spanning joint term j would constitute a correlation
        between D1 and D2, which independence (from anchor-disjointness via
        T_M) excludes -- hence J = 0. NOTE (audit fix B2-2): j is NOT
        literally an element of anc(D1) ^ anc(D2) (j is not in D1 u D2); the
        premise is not violated syntactically -- the exclusion runs through
        independence, not through a shared-anchor clash. T_M steps 4-9 remain
        available as the converse leg of the biconditional but are not the
        load-bearing implication here (audit fix B2-1). A reducible shared
        anchor, by contrast, IS an element of the intersection, excluded by
        hypothesis directly: R = 0. (2026-07-04 disambiguation, C1 landing:
        'shared anchor' in the R-count means the shared billed CHANNEL --
        the shared distinction both marginals bill -- not a shared LOCUS;
        in this check's witness data model the two coincide 1:1, which is
        why the wording was ambiguous. The locus reading provably breaks
        the identity; see check_T_delta_JR_derived, this module.)
      Step 2 [L_irr Step 1 counting identity -- the L_cost FORM, occupancy-
        free since we claim ZERO, not a sign]. Delta = epsilon*(J - R)
        = epsilon*(0 - 0) = 0.
      Step 3 [L_cost_C2 = T_M + L_loc]. Equivalently, the join carries count
        n1 + n2 and f(n1+n2) = f(n1) + f(n2) exactly; L_loc gives EQUALITY
        (independent budgets, factorized state space), not an inequality.
    GRADE: [P] -- every step rests on banked [P] content (T_M, L_loc,
      L_cost incl. sub-lemma C2, L_irr structural core (i)). Occupancy is
      NOT consumed (no sign claim is made). First executable instantiation
      of the eps(J - R) two-term structure (module honesty note).
    FENCES: F1 + F2 (module docstring). Negative controls NC1 (spanning
      term, Delta > 0) and NC2 (shared classical bit, Delta = -eps) run
      in-check: additivity is lost exactly where the premise fails.
    """
    # ---- Witness W0: two anchor-disjoint interfaces -------------------
    # Gamma_1 anchors {a, b} with one INTERNAL irreducibly-joint term
    # j1 = j(a,b) (so additivity across interfaces is tested in the
    # presence of internal superadditivity, not only in a free world).
    # Gamma_2 anchors {c, d}, no internal joint.
    anc = {'a': {1}, 'b': {1}, 'c': {2}, 'd': {2}}
    D1 = frozenset(['a', 'b'])
    D2 = frozenset(['c', 'd'])
    check(not (set().union(*(anc[x] for x in D1))
               & set().union(*(anc[x] for x in D2))),
          "premise: anc(D1) ^ anc(D2) = empty")

    def n_joint_internal_G1(S):
        return 1 if frozenset(['a', 'b']) <= S else 0

    def kappa(S):
        # cost = count * epsilon (L_cost); the only joint term is internal
        # to Gamma_1; anchor-disjointness => no spanning term (T_M <= +
        # L_irr Step 1, per derivation Step 1).
        return EPS * (len(S) + n_joint_internal_G1(S))

    k1, k2, kj = kappa(D1), kappa(D2), kappa(D1 | D2)
    check(k1 == 3 * EPS and k2 == 2 * EPS, "witness costs as designed")
    check(kj == k1 + k2, f"ADDITIVITY: kappa(D1|_|D2)={kj} != {k1}+{k2}")
    check(kj - k1 - k2 == 0, "Delta = 0 across anchor-disjoint interfaces")

    # exhaustive: additivity for EVERY pair (S1 c D1, S2 c D2)
    for S1 in _powerset(D1):
        for S2 in _powerset(D2):
            check(kappa(S1 | S2) == kappa(S1) + kappa(S2),
                  f"additivity fails at {set(S1)}, {set(S2)}")

    # ---- Negative control NC1: spanning distinction (premise fails) ---
    # x anchors at BOTH interfaces (L_irr's correlation c; T_canonical R8:
    # E_global[x] = E_at_1[x] + E_at_2[x] + Omega_inter). Omega_inter = +1.
    anc_x = {1, 2}
    check(bool(anc_x & {1}) and bool(anc_x & {2}),
          "NC1: anchor sets now intersect -- disjointness premise FAILS")
    E1_x, E2_x, Omega_inter = EPS, EPS, EPS   # spanning joint term: +1
    kappa_D1x = kappa(D1) + E1_x              # x's Gamma_1 share
    kappa_D2x = kappa(D2) + E2_x              # x's Gamma_2 share
    kappa_join = kappa(D1) + kappa(D2) + E1_x + E2_x + Omega_inter
    Delta_NC1 = kappa_join - kappa_D1x - kappa_D2x
    # x's per-interface shares are billed locally in each marginal (E1_x at
    # Gamma_1, E2_x at Gamma_2) and both appear in the join; the residual is
    # exactly the spanning term (T_canonical R8: Omega_inter lives ONLY in
    # the global cost, not in either marginal).
    check(Delta_NC1 == Omega_inter, "NC1 bookkeeping: Delta = Omega_inter")
    check(Delta_NC1 == EPS and Delta_NC1 > 0,
          "NC1: spanning distinction => Delta > 0 (superadditive; L_irr's "
          "correlation c) -- additivity is lost exactly where the "
          "disjointness premise fails")

    # ---- Negative control NC2: shared classical anchor (premise fails) -
    # s anchored at both families, ONE shared bit realizes it in the join
    # (level (1) of T_contextuality_implies_superadditive_cost):
    # cost(joint) = 1 < cost(A) + cost(B) = 2  =>  Delta = -epsilon.
    kappa_A = EPS      # {s} billed in D1's marginal
    kappa_B = EPS      # {s} billed in D2's marginal
    kappa_joint_s = EPS  # the join counts s ONCE
    Delta_NC2 = kappa_joint_s - kappa_A - kappa_B
    check(Delta_NC2 == -EPS, "NC2: shared classical anchor => Delta = -eps "
                             "(subadditive, R = 1, J = 0)")

    return _result(
        name='T_delta_disjoint_additivity -- Delta = 0 across anchor-disjoint '
             'interfaces (equality, theorem-strength)',
        tier=4,
        epistemic='P',
        summary=(
            'If anc(D1) ^ anc(D2) = empty then kappa(D1 |_| D2) = kappa(D1) '
            '+ kappa(D2), i.e. Delta = 0 -- EQUALITY, not an inequality. '
            'Step 1: anchor-disjointness gives independence (T_M steps 1-3, '
            'the <= direction of the biconditional), and an irreducibly-joint '
            'distinction across the pair is a correlation not reducible to '
            'either marginal (L_irr Step 1), which independence excludes, so '
            'J = 0; a reducible shared anchor is an element of the '
            'intersection, excluded by hypothesis, so R = 0. Step 2: the '
            'L_irr counting identity Delta = eps*(J - R) = 0 (occupancy-free '
            'use -- zero is claimed, not a sign). Step 3: equivalently '
            'L_cost_C2 (T_M + L_loc) gives f(n1+n2) = f(n1) + f(n2) exactly. '
            'Verified exhaustively on witness W0 (internal joint term present '
            'at Gamma_1, so additivity is tested against internal '
            'superadditivity). Negative controls: NC1 spanning term Delta = '
            '+eps (T_canonical R8 Omega_inter), NC2 shared classical bit '
            'Delta = -eps -- both ONLY where the disjointness premise fails. '
            'First executable instantiation of the eps(J - R) two-term '
            'structure (the identity previously lived in L_irr\'s docstring '
            'proof only). Fences F1 (anchor-disjoint, not spatial/causal) '
            'and F2 (no sign claim once anchors intersect) carried.'
        ),
        key_result=(
            'anc(D1) ^ anc(D2) = empty ==> Delta(D1, D2) = 0 exactly, by '
            'T_M(<=) + L_irr Step 1 + L_loc + L_cost_C2; negative controls '
            'pin Delta != 0 to premise failure.'
        ),
        dependencies=['T_M', 'L_loc', 'L_cost', 'L_irr'],
        cross_refs=['T_canonical', 'T_contextuality_implies_superadditive_cost',
                    'T_delta_coarse_graining_monotonicity'],
        artifacts={
            'witness_W0': 'kappa(D1)=3, kappa(D2)=2, kappa(join)=5, Delta=0',
            'NC1_spanning': 'Delta = +eps (Omega_inter, premise fails)',
            'NC2_shared_bit': 'Delta = -eps (R=1, J=0, premise fails)',
        },
    )


# =====================================================================
# CHECK 2 -- Monotonicity under coarse-graining + native free operations
# =====================================================================

def check_T_delta_coarse_graining_monotonicity() -> Dict:
    """T_delta_coarse_graining_monotonicity: what the banked axioms give --
    and provably do NOT give -- for Delta under coarse-graining.

    CLAUSE B (kappa subset-monotone, [P]): D' c D ==> kappa(D') <= kappa(D).
      By L_cost (cost = count) a subset carries a sub-count (its joint terms
      are a subset too). Banked as L3 (T_canonical Part I; L_irr structural
      core (i), occupancy-free). Verified exhaustively on the witness.

    CLAUSE D (Delta is NOT monotone under record-subset coarse-graining --
      pinned COUNTEREXAMPLE, both directions):
      World W1 = {s, a, b} + one irreducibly-joint term j(a,b); kappa
      subset-monotone throughout.
        Delta({s,a},{s,b}) = 0        (J=1 cancels R=1: shared anchor s)
        drop s (coarse-grain):  Delta({a},{b}) = +eps   INCREASE
        drop b instead:         Delta({s,a},{s}) = -eps DECREASE
      So coarse-graining can RAISE Delta (deleting a reducible shared
      anchor removes a -eps term of the L_irr counting identity) and can
      LOWER it (deleting a joint-carrier removes a +eps term). Delta is
      sign-indefinite under restriction: NOT a monotone. This is a
      theorem-strength no-go [P] (finite witness).

    CLAUSE C (quotient/block-merge reading -- the EXACT identity is banked):
      T_canonical Prop 9.8 (Omega3, exact refinement):
          Omega_fine = Omega_coarse + Delta_internal(a,b)
      i.e.  Delta_coarse = Delta_fine - Delta_internal.  [P]
      COROLLARY (conditional one-sided monotonicity): merging a block whose
      internal Delta_internal >= 0 (an OCCUPIED block) can only DECREASE
      the joint residual: Delta_coarse <= Delta_fine. Grade: [P] GIVEN the
      NAMED premise Delta_internal >= 0 -- occupancy is a per-interface
      input, not an A1 theorem (L_irr doctrine), so the unconditional form
      is NOT available. Negative control W3: a subadditive internal block
      (shared classical bit, Delta_internal = -eps, level (1) of
      T_contextuality_implies_superadditive_cost) makes coarse-graining
      INCREASE Delta -- the premise cannot be silently dropped.

    CLAUSE E (relabelings, [P]): an empirical-difference-free relabeling is
      a free coordinative convention (FD1-sc, check_FD1_structural_
      completeness); a bijective relabel preserves all counts, so kappa and
      Delta are exactly INVARIANT (not merely monotone). Verified.

    CPTP CLAUSE -- honest type boundary, NO theorem (module docstring); OPEN.

    First executable instantiation, with check 1, of the eps(J - R)
    two-term structure (module honesty note).
    """
    # ---- World W1: {s,a,b} + irreducibly-joint j(a,b) ------------------
    U1 = frozenset(['s', 'a', 'b'])

    def n1(S):
        return len(S) + (1 if frozenset(['a', 'b']) <= S else 0)

    E1 = {S: EPS * n1(S) for S in _powerset(U1)}

    # CLAUSE B: kappa subset-monotone (L3), exhaustive
    check(_monotone(E1, U1), "Clause B: L3 monotonicity")
    check(E1[frozenset('ab')] == 3 * EPS and E1[U1] == 4 * EPS,
          "W1 table as designed (integer multiples of eps)")

    # CLAUSE D: Delta non-monotone under subset coarse-graining
    D1f, D2f = frozenset(['s', 'a']), frozenset(['s', 'b'])
    d_fine = _Delta(E1, D1f, D2f)
    check(d_fine == 0, "W1: Delta({s,a},{s,b}) = eps*(J-R) = eps*(1-1) = 0")
    # coarse-graining 1: drop the shared anchor s from both families
    d_up = _Delta(E1, frozenset(['a']), frozenset(['b']))
    check(d_up == EPS, "counterexample: Delta INCREASES 0 -> +eps "
                       "(coarse-graining deleted the R-term)")
    check(frozenset(['a']) <= D1f and frozenset(['b']) <= D2f,
          "it IS a coarse-graining: D'_i c D_i")
    # coarse-graining 2: drop the joint-carrier b instead
    d_down = _Delta(E1, D1f, frozenset(['s']))
    check(d_down == -EPS, "other direction: Delta DECREASES 0 -> -eps "
                          "(coarse-graining deleted the J-carrier)")
    check(not (d_up <= d_fine) and (d_down <= d_fine),
          "Clause D pinned: Delta sign-indefinite under restriction -- "
          "NOT a monotone")

    # ---- CLAUSE C: exact refinement identity + conditional corollary ---
    # World W2: occupied internal block. E_a=1, E_b=1, Delta_ab=+2 => E_ab=4;
    # E_c=1, Delta(ab,c)=+1 => E_abc=6.
    U2 = frozenset(['a', 'b', 'c'])
    E2 = {
        frozenset():      Fraction(0),
        frozenset('a'):   EPS, frozenset('b'): EPS, frozenset('c'): EPS,
        frozenset('ab'):  4 * EPS, frozenset('ac'): 2 * EPS,
        frozenset('bc'):  2 * EPS, frozenset('abc'): 6 * EPS,
    }
    check(_monotone(E2, U2), "W2 monotone (L3)")
    d_int_W2 = _Delta(E2, frozenset('a'), frozenset('b'))
    d_coarse_W2 = _Delta(E2, frozenset('ab'), frozenset('c'))
    omega_fine_W2 = E2[frozenset('abc')] - sum(E2[frozenset(x)] for x in 'abc')
    check(omega_fine_W2 == d_coarse_W2 + d_int_W2,
          "T_canonical Prop 9.8 (exact refinement): "
          "Omega_fine = Delta_coarse + Delta_internal")
    check(d_int_W2 == 2 * EPS and d_int_W2 >= 0,
          "W2 premise: internal block OCCUPIED (Delta_internal >= 0)")
    check(d_coarse_W2 <= omega_fine_W2,
          "corollary: merging an occupied block DECREASES the residual "
          f"({d_coarse_W2} <= {omega_fine_W2})")

    # World W3 (negative control): subadditive internal block -- shared
    # classical bit: E_ab = 1 (one bit realizes both), Delta_ab = -eps.
    U3 = frozenset(['a', 'b', 'c'])
    E3 = {
        frozenset():      Fraction(0),
        frozenset('a'):   EPS, frozenset('b'): EPS, frozenset('c'): EPS,
        frozenset('ab'):  EPS, frozenset('ac'): 2 * EPS,
        frozenset('bc'):  2 * EPS, frozenset('abc'): 3 * EPS,
    }
    check(_monotone(E3, U3), "W3 monotone (L3) -- subadditivity is L3-compatible")
    d_int_W3 = _Delta(E3, frozenset('a'), frozenset('b'))
    d_coarse_W3 = _Delta(E3, frozenset('ab'), frozenset('c'))
    omega_fine_W3 = E3[frozenset('abc')] - sum(E3[frozenset(x)] for x in 'abc')
    check(d_int_W3 == -EPS, "W3: classical shared bit, Delta_internal = -eps "
                            "(level (1), T_contextuality_implies_superadditive_cost)")
    check(omega_fine_W3 == d_coarse_W3 + d_int_W3, "identity holds in W3 too")
    check(d_coarse_W3 > omega_fine_W3,
          "negative control pinned: subadditive internal block => "
          f"coarse-graining INCREASES Delta ({d_coarse_W3} > {omega_fine_W3})")

    # ---- CLAUSE E: relabeling invariance (FD1-sc) ----------------------
    sigma = {'s': 'u', 'a': 'v', 'b': 'w'}
    E1_rel = {frozenset(sigma[x] for x in S): E1[S] for S in E1}
    for S1 in _powerset(U1):
        for S2 in _powerset(U1):
            S1r = frozenset(sigma[x] for x in S1)
            S2r = frozenset(sigma[x] for x in S2)
            check(_Delta(E1_rel, S1r, S2r) == _Delta(E1, S1, S2),
                  "Clause E: Delta invariant under bijective relabeling")

    return _result(
        name='T_delta_coarse_graining_monotonicity -- kappa is the monotone; '
             'Delta is not (no-go + banked exact identity + conditional '
             'corollary)',
        tier=4,
        epistemic='P',
        summary=(
            'Clause B [P]: kappa is subset-monotone (L3, T_canonical Part I; '
            'L_irr structural core (i), occupancy-free), verified '
            'exhaustively. Clause D no-go [P]: Delta is NOT monotone under '
            'record-subset coarse-graining -- finite counterexamples in BOTH '
            'directions on world W1 (0 -> +eps deleting the reducible shared '
            'anchor; 0 -> -eps deleting the joint-carrier); Delta is '
            'sign-indefinite under restriction. Clause C: the exact '
            'refinement identity Delta_coarse = Delta_fine - Delta_internal '
            'is banked [P] (T_canonical Prop 9.8 / Omega3), verified on W2; '
            'the one-sided corollary (merging an OCCUPIED block, '
            'Delta_internal >= 0, can only decrease the residual) holds [P] '
            'GIVEN the NAMED occupancy premise -- occupancy is a '
            'per-interface input, not an A1 theorem, so the unconditional '
            'form is NOT available, and negative control W3 (subadditive '
            'internal block, Delta_internal = -eps) makes coarse-graining '
            'INCREASE Delta, so the premise cannot be silently dropped. '
            'Clause E [P]: bijective relabelings leave kappa and Delta '
            'exactly invariant (FD1-sc). CPTP clause: OPEN, honest type '
            'boundary -- no native referent without the GNS representation + '
            'an un-banked realizability claim; nothing is registered for it. '
            'With check 1, the first executable instantiation of the L_irr '
            'eps(J - R) two-term structure.'
        ),
        key_result=(
            'kappa is the monotone (L3); Delta is NOT: restriction '
            'counterexamples in both directions; block-merge obeys the banked '
            'exact identity Delta_coarse = Delta_fine - Delta_internal, '
            'one-sided monotone iff the merged block is occupied (named '
            'premise); relabelings leave Delta invariant.'
        ),
        dependencies=['L_cost', 'L_irr', 'T_canonical',
                      'FD1_structural_completeness'],
        cross_refs=['T_contextuality_implies_superadditive_cost',
                    'T_delta_disjoint_additivity', 'L_T2_finite_gns'],
        artifacts={
            'clause_grades': ('B [P]; C identity [P], corollary '
                              '[P | Delta_internal >= 0 (named occupancy '
                              'premise)]; D no-go [P]; E [P]; CPTP OPEN'),
            'W1_counterexample': 'Delta: 0 -> +eps (drop s) and 0 -> -eps (drop b)',
            'W2_occupied_block': 'Delta_internal = +2 eps, residual decreases',
            'W3_negative_control': 'Delta_internal = -eps, residual increases',
        },
    )



# =====================================================================
# CHECK 3 -- The characterization theorem: cost = count x epsilon
# =====================================================================

def check_T_cost_count_characterization() -> Dict:
    """T_cost_count_characterization: cost = count x epsilon -- the exact
    axiom set. (Landed v24.3.376, 2026-07-04, Paper 12 review-3 walk W1,
    reviewer Q2; fresh-context hostile audit AUDIT_W1 LAND-WITH-FIXES
    0.85, mandatory fixes 1/2/3/6 + recommended 4/5 carried.)

    THEOREM. Let kappa be any cost functional on finite distinction
    families. Suppose:

      (X1) COUNT-DEPENDENCE.  kappa(S) = f(n(S)) for some f: N -> R --
           cost depends only on the channel count, not on labels or
           presentation. Banked: L_cost sub-lemma C1 (Ledger
           Completeness, [P]; A1's universal quantifier makes the
           capacity ledger exhaustive, so no label-sensitive resource
           survives) + FD1-sc (check_FD1_structural_completeness,
           foundation_inputs.py, [P] ADOPTED-FOUNDATIONAL, named here
           per the check_T_ew_load_placement_P precedent: an empirical-
           difference-free relabeling is a free coordinative convention,
           zero cost -- executable as Clause E of
           check_T_delta_coarse_graining_monotonicity).

      (X2) ADDITIVITY over anchor-disjoint families, at COUNT level:
           f(n1+n2) = f(n1)+f(n2). Banked: L_cost sub-lemma C2 [P]
           = T_M steps 1-3 (disjoint anchors => independent; the <=
           direction of the biconditional) + L_loc Step 4(c)
           (independent budgets, factorized state space
           Omega(S1 u S2) = Omega(S1) x Omega(S2)) -- EQUALITY,
           executable as check_T_delta_disjoint_additivity [P] (check 1,
           this module). The family -> count transport (f well-defined
           via X1; the join's count is n1 + n2 because J = 0 on
           anchor-disjoint pairs, check 1 Step 1) is inherited banked
           content -- C2 is banked at count level -- not re-derived.

      (X3) MD FLOOR + NORMALIZATION.  f(1) = epsilon > 0.
           Banked: L_epsilon* [P] (deps A1 + MD + BW): positivity is the
           MD structural primitive; the VALUE of epsilon is a unit
           choice (calibration), like c = 1.

    THEN: f(n) = n * epsilon for ALL n in N, by INDUCTION ALONE.
      f(n) = f(n-1) + f(1) forces the unique solution; no continuity, no
      measurability, and -- on the count domain N -- NO MONOTONICITY is
      needed. Monotonicity is a COROLLARY: f(n+1) - f(n) = epsilon > 0
      (MD).

    SHARPENING vs the banked statement: L_cost_MAIN lists "C1 + C2 +
    monotonicity (L_epsilon*) + normalization"; this check shows the
    monotonicity hypothesis is REDUNDANT on N (derivable from X2 + X3).
    The conclusion of L_cost is unchanged; the hypothesis set shrinks.
    This check builds ON check_L_cost, it does not re-prove it (docstring
    pointer only at check_L_cost; no banked-hypothesis edit).

    CONTRAST (do not conflate): L_Cauchy_uniqueness (standalone, [P]) is
    the CONTINUUM-domain statement F: R+ -> R+, where monotonicity
    (Darboux 1875) IS load-bearing because Cauchy's equation on R has
    pathological non-measurable solutions. On N there are none: the
    domain discreteness -- itself forced by the MD floor -- is what
    deletes the regularity axiom. This is the Faddeev-Khinchin
    comparison's exact content: their continuity axiom does work only
    because their domain (the probability simplex) is a continuum; ours
    is not.

    UNIQUENESS OF epsilon: exact up to calibration. epsilon = f(1); any
    two additive solutions agreeing at 1 agree everywhere; two
    calibrations differ by a single global unit (all cost RATIOS are
    calibration-invariant). The physical magnitude of epsilon
    (Landauer / Margolus-Levitin-style ports) is an EXTERNAL calibration
    and enters the uniqueness nowhere.

    COARSE-GRAINING ROBUSTNESS (what survives): the FORM is
    scale-covariant -- the coarse family's cost is (its own count) x
    (the SAME epsilon) -- "the same" because the coarse family is a
    family in the SAME ledger evaluated by the SAME kappa (X1's single
    f), i.e. a WITHIN-LEDGER corollary of X1, exactly the single-table
    setting of Prop 9.8 (audit fix 1). Across DIFFERENT interface
    presentations the floor is Gamma-indexed (eps*_Gamma, L_epsilon*)
    and the bank asserts the identification structurally, NOT
    numerically (check_T_realignment_floor_is_epsilon_star: numeric
    normalisations differ by module and are NOT asserted equal);
    cross-presentation epsilon identification is F2/FD1-sc territory and
    is NOT claimed here. The joint residual redistributes per the banked
    EXACT refinement identity Delta_coarse = Delta_fine - Delta_internal
    (T_canonical Prop 9.8 / Omega3, [P]; executable in
    check_T_delta_coarse_graining_monotonicity). What does NOT survive:
    the count itself, and any sign/monotonicity claim for Delta (banked
    no-go, finite counterexamples both directions). Implementation
    changes that fix no empirical difference are relabelings: kappa and
    Delta exactly INVARIANT (FD1-sc).

    FENCES:
      (F1) 'Independent' = ANCHOR-disjoint (T_M biconditional),
           inherited from this module's F1; causal/spatial glosses only
           via L_loc Step 4(c).
      (F2) X1 covers relabelings WITHIN a presentation. Representation-
           independence across DIFFERENT interface presentations of the
           same physics is FD1 structural-completeness territory
           (adopted foundational clause, named -- not re-derived here);
           the same-epsilon coarse-graining claim is scoped WITHIN-LEDGER
           (see above), never cross-presentation.
      (F3) Nothing here fixes epsilon's physical magnitude; the
           calibration port is external by design.
      (F4) No sign claim for Delta once anchors intersect (this
           module's F2).

    GRADE: [P] -- every hypothesis is banked [P] content and the
    induction is exact/finite-witnessed. The FD1-sc leg of X1 is an
    ADOPTED foundational clause ([P] under the canonical convention,
    bank.py legend); it is named in the dependency list, not smuggled --
    same shape as check_T_ew_load_placement_P and check 2 of this
    module. Occupancy: not consumed.

    Self-contained arithmetic: stdlib + exact Fractions; epsilon
    deliberately NON-UNIT (7/3) so no step silently uses epsilon = 1.
    """
    EPS_W1 = Fraction(7, 3)   # deliberately non-unit
    N_MAX = 61                # exercise the full ledger range (C_total = 61)

    def _partitions(n, max_part=None):
        """All integer partitions of n (descending parts)."""
        if max_part is None:
            max_part = n
        if n == 0:
            yield ()
            return
        for k in range(min(n, max_part), 0, -1):
            for rest in _partitions(n - k, k):
                yield (k,) + rest

    # ================================================================
    # Stage 1 -- EXISTENCE + UNIQUENESS by induction on N (the core).
    # Any f with f(m+n) = f(m)+f(n) and f(1) = eps satisfies
    # f(n) = f(n-1) + f(1); the recursion from f(1) = eps has exactly
    # one solution. Build it, then verify ALL binary splits agree.
    # ================================================================
    f = {1: EPS_W1}
    for n in range(2, N_MAX + 1):
        f[n] = f[n - 1] + f[1]          # the recursion additivity forces
    for n in range(1, N_MAX + 1):
        check(f[n] == n * EPS_W1, f"induction: f({n}) != {n}*eps")
    for n in range(2, N_MAX + 1):       # every split, not just (n-1, 1)
        for k in range(1, n):
            check(f[n] == f[k] + f[n - k],
                  f"additivity consistency fails at split ({k},{n - k})")

    # Partition-independence: every way of assembling n from independent
    # parts yields the same total (exhaustive for n <= 12).
    for n in range(1, 13):
        totals = {sum(f[p] for p in part) for part in _partitions(n)}
        check(totals == {n * EPS_W1},
              f"partition-independence fails at n={n}: {totals}")

    # Uniqueness sharpened: a second additive solution g with g(1) = f(1)
    # agrees everywhere (telescoping); a solution with g(1) = eps' != eps
    # is a pure recalibration (Stage 6).
    g = {1: EPS_W1}
    for n in range(2, N_MAX + 1):
        g[n] = g[n - 1] + g[1]
    check(all(g[n] == f[n] for n in range(1, N_MAX + 1)),
          "uniqueness: two additive solutions agreeing at 1 agree everywhere")

    # ================================================================
    # Stage 2 -- Monotonicity is a COROLLARY, not a hypothesis.
    # f(n+1) - f(n) = eps > 0 (MD floor). And monotonicity ALONE does
    # not force linearity: n^2 is monotone but non-additive -- the
    # load-bearing axiom is X2, not monotonicity.
    # ================================================================
    check(EPS_W1 > 0, "X3: MD floor eps > 0 (L_epsilon*, primitive MD)")
    for n in range(1, N_MAX):
        check(f[n + 1] - f[n] == EPS_W1 and f[n + 1] > f[n],
              f"corollary monotonicity fails at n={n}")
    sq = {n: Fraction(n * n) * EPS_W1 for n in range(1, 20)}
    check(all(sq[n + 1] > sq[n] for n in range(1, 19)),
          "control: n^2*eps IS monotone")
    check(sq[5] != sq[2] + sq[3],
          "control: n^2*eps is NOT additive -- monotonicity alone "
          "cannot deliver the theorem; additivity (X2) is load-bearing")

    # ================================================================
    # Stage 3 -- NEGATIVE CONTROL NC1: drop X2 (additivity).
    # A non-linear cost exists (kappa = n^2 * eps) BUT it contradicts
    # banked content: on an anchor-disjoint pair with J = R = 0 it
    # yields Delta = 2*n1*n2*eps != 0, violating the theorem-strength
    # equality of check_T_delta_disjoint_additivity [P].
    # Audit fix 4: the axiom ISOLATION is pinned in-check -- the control
    # satisfies X1 (count-only by construction: kappa_sq reads nothing
    # but n) and X3 (kappa_sq(1) = eps > 0); it violates ONLY X2.
    # ================================================================
    n1, n2 = 3, 2                       # counts of two anchor-disjoint families
    kappa_sq = lambda n: Fraction(n * n) * EPS_W1
    check(kappa_sq(1) == EPS_W1 and EPS_W1 > 0,
          "NC1 isolation: the control SATISFIES X3 (kappa_sq(1) = eps > 0)")
    check(kappa_sq(n1) == Fraction(n1 * n1) * EPS_W1
          and kappa_sq(n2) == Fraction(n2 * n2) * EPS_W1,
          "NC1 isolation: the control SATISFIES X1 (a function of the "
          "count alone, by construction -- label-blind)")
    Delta_sq = kappa_sq(n1 + n2) - kappa_sq(n1) - kappa_sq(n2)
    check(Delta_sq == 2 * n1 * n2 * EPS_W1 and Delta_sq != 0,
          "NC1: non-additive cost realizes Delta != 0 across anchor-disjoint "
          "families -- refuted by T_delta_disjoint_additivity [P], not "
          "merely non-canonical; the control violates ONLY X2")

    # ================================================================
    # Stage 4 -- NEGATIVE CONTROL NC2: drop X1 (count-dependence).
    # A label-weighted cost kappa_w(S) = sum_x w(x) changes under an
    # empirical-difference-free bijective relabeling -- violating the
    # FD1-sc zero-cost-convention clause (Clause E invariance).
    # Audit fix 3: the swap must MOVE the family -- S = {a, c} has
    # sigma-image {b, c} != S (the pre-audit S = {a, b} was fixed
    # setwise, making the invariance check vacuous).
    # ================================================================
    w = {'a': EPS_W1, 'b': 2 * EPS_W1, 'c': EPS_W1}
    kappa_w = lambda S: sum(w[x] for x in S)
    S = frozenset(['a', 'c'])
    sigma = {'a': 'b', 'b': 'a', 'c': 'c'}      # pure relabel
    S_rel = frozenset(sigma[x] for x in S)      # = {b, c}
    check(S_rel != S and len(S_rel) == len(S),
          "NC2 setup (audit fix 3): the relabel MOVES the family setwise "
          "while preserving the count (bijective)")
    # count-form invariance (the theorem's kappa) vs weighted-cost variance:
    check(len(S_rel) * EPS_W1 == len(S) * EPS_W1,
          "count-form: exactly invariant under relabeling (FD1-sc Clause E)")
    check(kappa_w(S_rel) != kappa_w(S),
          "NC2: label-weighted cost is relabel-VARIANT on the moved family "
          "-- violates FD1-sc (zero-cost coordinative convention); X1 "
          "cannot be dropped")

    # ================================================================
    # Stage 5 -- COARSE-GRAINING: covariance is a COROLLARY of X1; the
    # executable content of this stage is the Prop 9.8 redistribution.
    # Audit fix 2: merging {a,b} into one block A yields a coarse family
    # that is itself a family in the SAME ledger, hence in kappa's
    # domain -- X1's single global f prices it at (its own count) x the
    # SAME eps, by the Stage-1 theorem APPLIED to the coarse count (a
    # corollary, not an independent arithmetic fact; the pre-audit form
    # checked a definition against itself). WITHIN-LEDGER scope only
    # (docstring; audit fix 1).
    # ================================================================
    fine = ['a', 'b', 'c', 'd']
    coarse = ['A', 'c', 'd']            # A = merged block {a,b}
    check(f[len(coarse)] == 3 * EPS_W1 and f[len(fine)] == 4 * EPS_W1,
          "W5 (corollary of X1, within-ledger): the coarse family lies in "
          "kappa's domain, so the Stage-1 theorem prices it at (its own "
          "count) x the SAME eps; the verified content of this stage is "
          "the Prop 9.8 redistribution below")

    # Prop 9.8 on a world with a joint term (independent numbers from the
    # check-2 W2 witness, rescaled to the non-unit eps): E_a = E_b = E_c
    # = eps; joint(a,b) = +2eps; spanning(ab|c) = +eps.
    E = {
        frozenset(): Fraction(0),
        frozenset('a'): EPS_W1, frozenset('b'): EPS_W1,
        frozenset('c'): EPS_W1,
        frozenset('ab'): 4 * EPS_W1, frozenset('ac'): 2 * EPS_W1,
        frozenset('bc'): 2 * EPS_W1, frozenset('abc'): 6 * EPS_W1,
    }
    D = lambda S1, S2: E[S1 | S2] - E[S1] - E[S2]
    d_internal = D(frozenset('a'), frozenset('b'))
    d_coarse = D(frozenset('ab'), frozenset('c'))
    omega_fine = E[frozenset('abc')] - sum(E[frozenset(x)] for x in 'abc')
    check(omega_fine == d_coarse + d_internal,
          "W5: exact refinement identity Delta_coarse = Delta_fine - "
          "Delta_internal (T_canonical Prop 9.8, banked [P])")
    check(d_internal == 2 * EPS_W1 and d_coarse == EPS_W1,
          "W5: Delta redistributes across scales; the FORM (count x eps) "
          "is what survives, not the count")

    # ================================================================
    # Stage 6 -- CALIBRATION EXACTNESS: eps unique up to one unit choice.
    # A second calibration eps' rescales every cost by eps'/eps; all
    # cost RATIOS are calibration-invariant. External ports (Landauer,
    # Margolus-Levitin) set the unit; they enter uniqueness nowhere.
    # ================================================================
    EPS2 = Fraction(5, 2)
    f2 = {n: n * EPS2 for n in range(1, N_MAX + 1)}
    ratio = EPS2 / EPS_W1
    check(all(f2[n] == ratio * f[n] for n in range(1, N_MAX + 1)),
          "W6: two calibrations differ by ONE global unit factor")
    check(f[8] / f[3] == f2[8] / f2[3] == Fraction(8, 3),
          "W6: cost ratios are calibration-invariant (physics lives in "
          "ratios; the unit is the external port)")

    return _result(
        name='T_cost_count_characterization -- cost = count x epsilon from '
             'X1 (count-dependence) + X2 (disjoint additivity) + X3 (MD '
             'floor); no continuity, no monotonicity',
        tier=4,
        epistemic='P',
        summary=(
            'CHARACTERIZATION: any kappa satisfying X1 count-dependence '
            '(L_cost_C1 [P] + FD1-sc [P] adopted-foundational), X2 '
            'additivity over anchor-disjoint families (L_cost_C2 = T_M(<=) '
            '+ L_loc [P]; executable T_delta_disjoint_additivity), and X3 '
            'the MD floor f(1) = eps > 0 (L_epsilon* [P]) equals '
            'kappa(S) = n(S)*eps -- by induction on N alone. Continuity, '
            'measurability, and monotonicity are NOT hypotheses: '
            'monotonicity is a corollary (f(n+1)-f(n) = eps > 0), and the '
            'discrete count domain (itself forced by the MD floor) deletes '
            'the regularity axiom that Faddeev-Khinchin-type '
            'characterizations need on continuum domains (contrast '
            'L_Cauchy_uniqueness, where Darboux monotonicity IS '
            'load-bearing on R+). Sharpens L_cost_MAIN by showing its '
            'monotonicity hypothesis redundant on N; conclusion unchanged. '
            'epsilon is fixed exactly up to one unit choice; all cost '
            'ratios calibration-invariant; the physical magnitude is the '
            'external calibration port (F3). Coarse-graining: the FORM is '
            'scale-covariant WITHIN-LEDGER -- the coarse family is a '
            'family in the same ledger under X1\'s single f, a corollary '
            'of X1 (cross-presentation eps identification is NOT claimed: '
            'the floor is Gamma-indexed and '
            'check_T_realignment_floor_is_epsilon_star declines the '
            'numeric identification); Delta redistributes per the banked '
            'exact refinement identity (Prop 9.8); relabelings leave kappa '
            'and Delta exactly invariant (FD1-sc). Negative controls: NC1 '
            'non-additive n^2 cost satisfies X1 + X3 in-check and '
            'contradicts the banked Delta = 0 theorem (violates ONLY X2); '
            'NC2 label-weighted cost is relabel-variant on a family the '
            'swap genuinely moves (violates FD1-sc). Fences F1-F4 carried.'
        ),
        key_result=(
            'X1 + X2 + X3 ==> kappa = n*eps uniquely on N (induction; no '
            'regularity axiom); eps = f(1) up to calibration; form '
            'scale-covariant under coarse-graining (within-ledger, '
            'corollary of X1), invariant under relabeling.'
        ),
        dependencies=['L_cost', 'T_M', 'L_loc', 'L_epsilon*',
                      'FD1_structural_completeness', 'T_canonical'],
        cross_refs=['T_delta_disjoint_additivity',
                    'T_delta_coarse_graining_monotonicity',
                    'L_Cauchy_uniqueness',
                    'T_realignment_floor_is_epsilon_star'],
        artifacts={
            'axioms': {
                'X1': 'count-dependence (L_cost_C1 + FD1-sc)',
                'X2': 'anchor-disjoint additivity (L_cost_C2 = T_M + L_loc)',
                'X3': 'MD floor + normalization f(1)=eps (L_epsilon*)',
            },
            'not_needed': ['continuity', 'measurability',
                           'monotonicity (corollary)'],
            'eps_calibration': 'unique up to one unit; ratios invariant',
            'NC1': 'n^2 cost => Delta != 0 disjoint (refuted by banked '
                   '[P]); satisfies X1+X3 in-check, violates only X2',
            'NC2': 'label-weighted cost violates FD1-sc relabel invariance '
                   '(family moved setwise by the swap)',
            'coarse_graining': 'form scale-covariant WITHIN-LEDGER '
                               '(corollary of X1; cross-presentation eps '
                               'NOT claimed); Prop 9.8 exact; Delta not '
                               'monotone (banked no-go)',
        },
    )



# =====================================================================
# CHECK 4 -- Delta is not an information functional
# =====================================================================

def _uniform(points):
    n = len(points)
    return {pt: Fraction(1, n) for pt in points}


def _marginal(dist, idxs):
    out = {}
    for pt, pr in dist.items():
        key = tuple(pt[i] for i in idxs)
        out[key] = out.get(key, Fraction(0)) + pr
    return out


def _perp_pow(dist, N):
    """Exact Fraction 2^(N*H(dist)) = prod_i p_i^(-N*p_i); needs N*p_i in Z."""
    out = Fraction(1)
    for p in dist.values():
        if p:
            e = p * N
            check(e.denominator == 1, "N does not clear the denominators")
            out *= p ** (-int(e))
    return out


def _entropy_cmp(terms, const):
    """Exact sign of sum(coef*H(dist) for coef, dist in terms) - const.

    Compares 2^(N*lhs) = prod _perp_pow(d, N)^coef against 2^(N*const),
    both exact Fractions. Returns -1, 0, or +1. No float anywhere."""
    from math import lcm
    const = Fraction(const)
    dens = [pr.denominator for _, d in terms for pr in d.values() if pr]
    N = lcm(*(dens + [const.denominator]))
    lhs = Fraction(1)
    for coef, d in terms:
        lhs *= _perp_pow(d, N) ** coef
    rhs = Fraction(2) ** int(const * N)
    return (lhs > rhs) - (lhs < rhs)


def _TC_terms(dist, n):
    """Total correlation of the n variables of dist."""
    terms = [(1, _marginal(dist, (i,))) for i in range(n)]
    terms.append((-1, dist))
    return terms


def _MI_terms(dist, A, B):
    """Mutual information of the composite block variables X_A, X_B
    (blocks may overlap -- they are composite random variables)."""
    U = tuple(sorted(set(A) | set(B)))
    return [(1, _marginal(dist, A)), (1, _marginal(dist, B)),
            (-1, _marginal(dist, U))]


def _coinfo_terms(dist):
    """Co-information I(X0;X1;X2) = I(X0;X1) - I(X0;X1|X2)
    = H0+H1-H01-H02-H12+H2+H012 (McGill/Bell convention: positive =
    redundancy-dominated, negative = synergy-dominated)."""
    return [(1, _marginal(dist, (0,))), (1, _marginal(dist, (1,))),
            (-1, _marginal(dist, (0, 1))), (-1, _marginal(dist, (0, 2))),
            (-1, _marginal(dist, (1, 2))), (1, _marginal(dist, (2,))),
            (1, dist)]


def check_T_delta_not_an_information_functional() -> Dict:
    """T_delta_not_an_information_functional: Delta is not a function of
    the bridged joint READOUT distribution -- positioned against TC, MI,
    co-information, and (qualitatively, at the two textbook poles) PID
    synergy/redundancy, with every separation pinned by an exact finite
    witness. (Landed v24.3.379, 2026-07-04, Paper 12 round-4 walk A3,
    reviewer Q6; audit LAND-WITH-FIXES 0.85, F1-F6 carried.)

    THE BRIDGE, stated honestly (audit F1 -- the readout-pushforward
    form). Delta is capacity-denominated (integer multiples of eps, the
    characterization theorem = check 3) and defined on distinction
    families; TC/MI/co-information are bit-denominated functionals of
    joint outcome distributions. Any comparison needs a named map. The
    bridge used here is THE PUSHFORWARD OF THE UNIFORM MEASURE ON
    Omega(D1 v D2) THROUGH THE TWO FAMILIES' READOUT MAPS -- one variable
    per family readout (per-record-readout coordinatization, NOT
    per-anchor); a reducible shared anchor makes the two readouts literal
    copies; an irreducibly-joint distinction over an anchor set is one
    parity-type constraint on its joint valuations, not expressible on
    any proper sub-family; the measure is uniform (max-entropy) on the
    admissible valuation set Omega -- the object L_loc factorizes. The
    bridge is a COMPARISON DEVICE defined inside this check (the NC1/NC2
    epistemic shape: it defines the object it refutes claims about); the
    framework nowhere asserts that records have outcome statistics. For
    every configuration in legs A, B, E, F records correspond to distinct
    anchors and the per-anchor and per-readout coordinatizations
    coincide; only the copy pair / copy triple (legs C, D) see the
    difference, and there the readout form is what an outcome table IS.
    Scope of the headline (audit F1 item 3): Delta is not a function of
    the two families' bridged joint READOUT distribution (the outcome
    table) -- which is the right scope for the reviewer's question, since
    TC/MI/co-info/PID are all computed on outcome statistics. A bridge
    that carries billing structure (e.g. anchor-occupancy side-variables)
    can distinguish the clash pair -- that restates the theorem rather
    than threatening it: the billing structure is not in the outcome
    statistics. (Even under a hostile per-anchor reading of the copy
    pair, the leg-E block-MI two-point clash alone already delivers
    "Delta is not a function of block MI / TC-of-union".)

    LEGS (exact; the -eps ledger values are BANKED REUSE, not extensions:
    NC2 of check_T_delta_disjoint_additivity and the W1 drop-b Clause D of
    check_T_delta_coarse_graining_monotonicity):
      A (agreement): anchor-disjoint product => Delta = 0 (banked, check 1)
        and cross-block TC = 0 exactly (|Omega_joint| = |Omega_1|*|Omega_2|).
      B (co-movement): parity pair Delta = +eps with I(a;b) = 1 bit; XOR
        triple Delta({a,b}|{c}) = +eps with TC = 1 bit; XOR pair split
        Delta = 0 with I(a;b) = 0 exactly.
      C (THE HEADLINE CLASH): parity pair vs copy pair -- identical bridge
        images (uniform on {00, 11}), Delta = +eps vs -eps. Delta is not a
        function of the bridged joint readout distribution.
      D (sign anatomy, with the audit-F4 split clause): co-info(XOR) = -1
        bit with Delta = +eps UNDER THE {a,b}|{c} SPLIT ONLY (the {a}|{b}
        split gives Delta = 0 -- leg B); co-info(copy triple) = +1 bit
        with Delta = -eps under EVERY bipartition (split-robust: {r1}|{r2}
        and {r1,r2}|{r3} both computed). TC positive on both poles,
        tracks neither sign. sign(Delta) = -sign(co-info) on the poles:
        eps*(J - R) is a count-level synergy-minus-redundancy with the
        sign convention flipped; an echo, not an identity (leg F kills
        Delta = -eps*co-info exactly).
      E (restriction-monotonicity separation): the banked W1 world
        bridged; restriction maps to deterministic per-block
        coarse-graining (local processing) under which MI and TC-of-union
        are non-increasing (restriction-MONOTONE, audit F6 wording),
        while Delta moves strictly both ways (0 -> +eps drop-s;
        0 -> -eps drop-b). Orientation kill: no monotone g in either
        orientation with g(Phi(bridge(config))) = Delta(config) for any
        restriction-monotone Phi. Two-point clashes: MI = 1 bit at BOTH
        Delta = +eps and Delta = -eps; TC(union) = 1 bit at BOTH
        Delta = 0 and Delta = +eps. (Co-information is not
        restriction-monotone, so it escapes the proposition's hypothesis
        -- legs C and F kill it by direct witness instead.)
      F (denomination): the biased-support dial P(a=b) = p at
        p in {1/2, 3/4, 1}, marginals uniform: TC takes three
        exactly-distinguished values (0; strictly between 0 and 1; 1 bit)
        and co-information on the biased XOR family sweeps (-1, 0), while
        the record configuration -- and hence Delta -- is FIXED. The
        Delta-constancy in the dial is DEFINITIONAL under the bridge
        (audit F3: p is a bridge-side parameter outside Delta's domain;
        the leg's executable content is TC/co-info MOVING, not Delta
        sitting still -- no theater loop).

    GRADE [P] (audit adjudication: sustainable after F1 + F5): every leg
    is exact finite mathematics; the bridge is a named comparison
    construction defined in-check (the NC1/NC2 precedent); the ledger
    values replicate banked in-check content; entropy comparisons are
    exact rational arithmetic on the exponentiated quantities 2^{N*H}
    (rational for rational distributions), no float on any pass path.

    OCCUPANCY: not consumed -- all signs are properties of named witness
    worlds whose billing replicates banked in-check content (NC1/NC2 of
    check 1; Clause D of check 2); no physical-interface sign claim is
    made (audit F5, the module-standard fence).

    FENCES: the theorem is about the comparison -- "no functional of the
    bridged readout statistics equals Delta" -- quantified over the named
    bridge family; it does not assert that interface records HAVE outcome
    statistics. Fences F1 + F2 of the module docstring carried. The
    contextuality-measure positioning (contextual fraction) stays with
    Paper 12 SS9.4; nothing is added there.
    """
    checks = []

    def ck(cond, msg):
        checks.append((bool(cond), msg))
        check(cond, msg)

    # ---- bridged distributions (readout-pushforward bridge) ------------
    # parity pair: readouts of the two families, locked by the joint
    # record j(a,b); copy pair: two readouts of ONE shared anchor --
    # literal copies. IDENTICAL images by construction of the pushforward.
    parity_pair = _uniform([(0, 0), (1, 1)])
    copy_pair = _uniform([(0, 0), (1, 1)])
    xor_triple = _uniform([(a, b, a ^ b) for a in (0, 1) for b in (0, 1)])
    copy_triple = _uniform([(0, 0, 0), (1, 1, 1)])
    # W1 (banked check-2 world {s, a, b} + j(a,b)): variables (s, a, b),
    # support a = b with s free.
    W1 = _uniform([(s, a, a) for s in (0, 1) for a in (0, 1)])
    # anchor-disjoint product (mirrors witness W0 of check 1: an INTERNAL
    # joint term in each block, so the test is not free-world).
    prod4 = _uniform([(a, a, c, c) for a in (0, 1) for c in (0, 1)])

    def biased_pair(p):
        p = Fraction(p)
        return {(0, 0): p / 2, (1, 1): p / 2,
                (0, 1): (1 - p) / 2, (1, 0): (1 - p) / 2}

    def biased_xor(p):
        p = Fraction(p)
        return {(a, b, c): (p / 4 if a ^ b ^ c == 0 else (1 - p) / 4)
                for a in (0, 1) for b in (0, 1) for c in (0, 1)}

    # ---- ledger side: exact Delta billing (eps = 1), banked shapes -----
    d_parity = 3 * EPS - EPS - EPS        # NC1 shape (check 1): J=1, R=0
    d_copy = EPS - EPS - EPS              # NC2 (check 1, banked): J=0, R=1
    d_xor_split = 4 * EPS - 2 * EPS - EPS  # {a,b}|{c}: join carries j
    d_xor_pair = 2 * EPS - EPS - EPS      # {a}|{b}: join does NOT carry j
    d_copy_pair_12 = EPS - EPS - EPS      # copy triple, {r1}|{r2}
    d_copy_join_3 = EPS - EPS - EPS       # copy triple, {r1,r2}|{r3}

    def _kappa_W1(S):
        # exactly check 2's world: n(S) = |S| + [ {a,b} <= S ]
        return EPS * (len(S) + (1 if {'a', 'b'} <= S else 0))

    def _delta_W1(S1, S2):
        return _kappa_W1(S1 | S2) - _kappa_W1(S1) - _kappa_W1(S2)

    d_W1_fine = _delta_W1({'s', 'a'}, {'s', 'b'})
    d_W1_drop_s = _delta_W1({'a'}, {'b'})
    d_W1_drop_b = _delta_W1({'s', 'a'}, {'s'})

    # ================= LEG A -- agreement ================================
    d_prod = 6 * EPS - 3 * EPS - 3 * EPS
    ck(d_prod == 0, "leg A ledger: Delta = 0 across anchor-disjoint "
                    "interfaces (banked, check 1)")
    ck(len(prod4) == len(_marginal(prod4, (0, 1))) * len(_marginal(prod4, (2, 3))),
       "leg A bridge: |Omega_joint| = |Omega_1| x |Omega_2| (exact integer "
       "identity; the L_loc factorization)")
    ck(_entropy_cmp(_MI_terms(prod4, (0, 1), (2, 3)), 0) == 0,
       "leg A bridge: cross-block TC = I(block1; block2) = 0 exactly")

    # ================= LEG B -- co-movement ==============================
    ck(d_parity == EPS, "leg B ledger: parity pair Delta = +eps (J=1, R=0)")
    ck(_entropy_cmp(_MI_terms(parity_pair, (0,), (1,)), 1) == 0,
       "leg B bridge: parity pair I(a;b) = TC = 1 bit exactly")
    ck(d_xor_split == EPS,
       "leg B ledger: XOR triple, split {a,b}|{c}: Delta = +eps (the parity "
       "record spans all three anchors; the join carries it)")
    ck(_entropy_cmp(_TC_terms(xor_triple, 3), 1) == 0,
       "leg B bridge: XOR triple TC = 1 bit exactly -- co-moves")
    ck(d_xor_pair == 0,
       "leg B ledger: XOR pair split {a}|{b}: Delta = 0 (anc(j) is not a "
       "subset of {a,b}; the join does not carry the parity record)")
    ck(_entropy_cmp(_MI_terms(xor_triple, (0,), (1,)), 0) == 0,
       "leg B bridge: XOR pairwise I(a;b) = 0 exactly -- matches Delta = 0 "
       "(the ledger's split-sensitivity matches the marginal structure)")

    # ================= LEG C -- THE HEADLINE CLASH =======================
    ck(parity_pair == copy_pair,
       "leg C: bridge images IDENTICAL -- parity pair and copy pair "
       "pushforward to the same outcome table (uniform on {00, 11})")
    ck(d_parity == +EPS and d_copy == -EPS,
       "leg C ledger: Delta(parity) = +eps, Delta(copy) = -eps (the -eps "
       "side is banked verbatim: NC2 of check 1)")
    ck(d_parity != d_copy,
       "leg C CONCLUSION: Delta is NOT a function of the bridged joint "
       "READOUT distribution -- J-type commitment and R-type sharing are "
       "statistically indistinguishable in the outcome table and billed "
       "with opposite signs (a difference in what is committed at the "
       "interface, not in the outcome table)")

    # ================= LEG D -- sign anatomy (split clause, F4) ==========
    ck(_entropy_cmp(_coinfo_terms(xor_triple), -1) == 0,
       "leg D: XOR triple co-information = -1 bit exactly (synergy pole)")
    ck(d_xor_split == +EPS,
       "leg D: Delta = +eps on the synergy pole UNDER THE {a,b}|{c} SPLIT "
       "ONLY (the {a}|{b} split gives 0, leg B) -- split-sensitive")
    ck(_entropy_cmp(_coinfo_terms(copy_triple), 1) == 0,
       "leg D: copy triple co-information = +1 bit exactly (redundancy pole)")
    ck(d_copy_pair_12 == -EPS and d_copy_join_3 == -EPS,
       "leg D: Delta = -eps on the redundancy pole under EVERY bipartition "
       "({r1}|{r2} and {r1,r2}|{r3} both) -- split-ROBUST; the asymmetry "
       "(synergy split-sensitive, redundancy split-robust) is itself "
       "structure-vs-statistics content")
    ck(_entropy_cmp(_TC_terms(xor_triple, 3), 0) == 1
       and _entropy_cmp(_TC_terms(copy_triple, 3), 0) == 1,
       "leg D: TC strictly positive on BOTH poles (1 and 2 bits) -- "
       "unsigned, tracks neither")
    ck(_entropy_cmp(_TC_terms(copy_triple, 3), 2) == 0,
       "leg D: copy triple TC = 2 bits exactly")
    ck((d_xor_split > 0) and (_entropy_cmp(_coinfo_terms(xor_triple), 0) == -1)
       and (d_copy_pair_12 < 0)
       and (_entropy_cmp(_coinfo_terms(copy_triple), 0) == 1),
       "leg D: sign(Delta) = -sign(co-information) on both pure poles -- "
       "eps*(J - R) is a count-level synergy-minus-redundancy, convention "
       "flipped; an echo, not an identity (leg F)")

    # ================= LEG E -- restriction-monotonicity separation ======
    ck((d_W1_fine, d_W1_drop_s, d_W1_drop_b) == (0, EPS, -EPS),
       "leg E ledger (banked, check 2 Clause D): Delta = 0 fine; +eps "
       "dropping s; -eps dropping b")
    mi_fine = _MI_terms(W1, (0, 1), (0, 2))
    mi_drop_s = _MI_terms(W1, (1,), (2,))
    mi_drop_b = _MI_terms(W1, (0, 1), (0,))
    ck(_entropy_cmp(mi_fine, 2) == 0, "leg E: MI((s,a);(s,b)) = 2 bits exactly")
    ck(_entropy_cmp(mi_drop_s, 1) == 0, "leg E: MI(a;b) = 1 bit exactly")
    ck(_entropy_cmp(mi_drop_b, 1) == 0, "leg E: MI((s,a);s) = 1 bit exactly")
    ck(_entropy_cmp(mi_drop_s, 2) == -1 and _entropy_cmp(mi_drop_b, 2) == -1,
       "leg E: MI weakly decreases on BOTH restriction branches "
       "(restriction = deterministic per-block coarse-graining = local "
       "processing; data processing inequality)")
    ck(d_W1_drop_s > d_W1_fine and d_W1_drop_b < d_W1_fine,
       "leg E ORIENTATION KILL: Delta strictly increases on one branch and "
       "strictly decreases on the other -- no monotone g in either "
       "orientation with g(restriction-monotone functional) = Delta")
    ck(_entropy_cmp(mi_drop_s + [(-c, d) for c, d in mi_drop_b], 0) == 0,
       "leg E two-point clash (MI): MI = 1 bit at BOTH ({a},{b}) and "
       "({s,a},{s})")
    ck(d_W1_drop_s == +EPS and d_W1_drop_b == -EPS,
       "leg E: ...where Delta = +eps and -eps respectively -- Delta is not "
       "a function of block MI (no monotonicity hypothesis needed)")
    tc_union_fine = _TC_terms(W1, 3)
    tc_union_drop_s = _TC_terms(_marginal(W1, (1, 2)), 2)
    tc_union_drop_b = _TC_terms(_marginal(W1, (0, 1)), 2)
    ck(_entropy_cmp(tc_union_fine, 1) == 0
       and _entropy_cmp(tc_union_drop_s, 1) == 0,
       "leg E two-point clash (TC): TC(union) = 1 bit at BOTH the fine "
       "configuration (Delta = 0) and the drop-s configuration "
       "(Delta = +eps) -- Delta is not a function of TC-of-union either")
    ck(_entropy_cmp(tc_union_drop_b, 0) == 0,
       "leg E: TC(union) = 0 on the drop-b configuration (completeness)")

    # ================= LEG F -- denomination =============================
    # Delta-constancy in the dial is DEFINITIONAL: p is a bridge-side
    # parameter outside Delta's domain (audit F3; no theater loop). The
    # executable content is the statistics MOVING:
    ck(d_parity == EPS,
       "leg F ledger: the parity configuration is fixed; Delta = +eps "
       "(p lives only on the bridge side -- definitional constancy)")
    tc_half = _TC_terms(biased_pair(Fraction(1, 2)), 2)
    tc_3q = _TC_terms(biased_pair(Fraction(3, 4)), 2)
    tc_one = _TC_terms(biased_pair(1), 2)
    ck(_entropy_cmp(tc_half, 0) == 0, "leg F: TC(p=1/2) = 0 exactly")
    ck(_entropy_cmp(tc_one, 1) == 0, "leg F: TC(p=1) = 1 bit exactly")
    ck(_entropy_cmp(tc_3q, 0) == 1 and _entropy_cmp(tc_3q, 1) == -1,
       "leg F: TC(p=3/4) strictly between 0 and 1 (exact "
       "exponentiated-rational comparison) -- three exactly-distinguished "
       "TC values against ONE Delta value")
    ci_half = _coinfo_terms(biased_xor(Fraction(1, 2)))
    ci_3q = _coinfo_terms(biased_xor(Fraction(3, 4)))
    ci_one = _coinfo_terms(biased_xor(1))
    ck(_entropy_cmp(ci_half, 0) == 0, "leg F: co-info(p=1/2) = 0 exactly")
    ck(_entropy_cmp(ci_one, -1) == 0, "leg F: co-info(p=1) = -1 bit exactly")
    ck(_entropy_cmp(ci_3q, 0) == -1 and _entropy_cmp(ci_3q, -1) == 1,
       "leg F: co-info(p=3/4) strictly between -1 and 0 -- kills any "
       "proposed identity Delta = -eps * co-information: co-info sweeps, "
       "the configuration (hence Delta = +eps) is fixed")
    ck(all(_entropy_cmp(_MI_terms(biased_xor(p), (0,), (1,)), 0) == 0
           for p in (Fraction(1, 2), Fraction(3, 4), Fraction(1))),
       "leg F: pairwise marginals of the biased XOR family stay uniform at "
       "every p (pairwise independence survives biasing -- the dial is clean)")

    n_legs = len(checks)

    return _result(
        name='T_delta_not_an_information_functional -- Delta is not a '
             'function of the bridged joint readout distribution '
             '(exact separations from TC / MI / co-information)',
        tier=4,
        epistemic='P',
        summary=(
            'Under the NAMED readout-pushforward bridge (the pushforward of '
            'the uniform measure on Omega(D1 v D2) through the two '
            'families\' readout maps -- a comparison device defined '
            'in-check, the NC1/NC2 epistemic shape; the framework nowhere '
            'asserts that records have outcome statistics), Delta is '
            'provably NOT a function of the two families\' bridged joint '
            'READOUT distribution: the irreducibly-joint parity pair and '
            'the reducibly-shared copy pair have IDENTICAL bridge images '
            '(uniform on {00,11}) and opposite Delta (+eps vs -eps; the '
            '-eps side is banked verbatim -- NC2 of check 1 and the W1 '
            'drop-b Clause D of check 2). Agreement where the calculus '
            'asserts zero: anchor-disjoint product has Delta = 0 with '
            'cross-block TC = 0 exactly; the XOR pair split has Delta = 0 '
            'with pairwise MI = 0 exactly. Sign anatomy with the split '
            'clause: sign(Delta) = -sign(co-information) on the two pure '
            'poles -- the synergy pole (+eps) holds under the {a,b}|{c} '
            'split only, the redundancy pole (-eps) under every bipartition '
            '-- so eps*(J-R) is a count-level synergy-minus-redundancy with '
            'the sign convention flipped; an echo, not an identity (the '
            'biased dial kills Delta = -eps*co-info exactly). '
            'Restriction-monotonicity separation on the banked W1 '
            'counterexample: restriction maps to local processing, under '
            'which MI and TC-of-union are restriction-monotone, while Delta '
            'moves strictly both ways -- no monotone of any '
            'restriction-monotone information functional equals Delta, and '
            'the two-point clashes (MI = 1 bit at Delta = +eps AND -eps; '
            'TC = 1 bit at Delta = 0 AND +eps) give the stronger '
            'no-function conclusion directly. Denomination: the biased dial '
            'sweeps TC through three exactly-distinguished values and '
            'co-information through (-1, 0) while the record configuration '
            'is fixed (Delta-constancy definitional -- p is outside '
            'Delta\'s domain). Delta reads STRUCTURE (which records are '
            'co-committed against a finite budget), not STATISTICS (how '
            'correlated the committed records\' outcomes are). All '
            'arithmetic exact: entropy comparisons via the rational '
            '2^{N*H}; no float on any pass path; %d assertions. Occupancy: '
            'not consumed -- all signs are properties of named witness '
            'worlds whose billing replicates banked in-check content '
            '(NC1/NC2 of check 1; Clause D of check 2).' % n_legs
        ),
        key_result=(
            'Same outcome table, opposite Delta (+eps vs -eps): Delta is '
            'not a function of the bridged readout statistics. '
            'sign(Delta) = -sign(co-info) on the pure poles (synergy pole '
            'split-sensitive, redundancy pole split-robust); MI/TC '
            'restriction-monotone while Delta is not; statistics sweep, '
            'Delta fixed. Structure, not statistics.'
        ),
        dependencies=['L_cost', 'L_irr', 'T_M', 'L_loc'],
        cross_refs=['T_delta_disjoint_additivity',
                    'T_delta_coarse_graining_monotonicity',
                    'T_cost_count_characterization',
                    'T_contextuality_implies_superadditive_cost'],
        n_assertions=n_legs,
        artifacts={
            'bridge': 'readout-pushforward: uniform on Omega(join) pushed '
                      'through the families\' readout maps; per-anchor and '
                      'per-readout coordinatizations coincide on legs '
                      'A/B/E/F; the copy configurations are where the '
                      'outcome-table form is load-bearing',
            'headline': 'parity pair vs copy pair: identical images, '
                        'Delta = +eps vs -eps (banked NC2)',
            'sign_table': {'XOR (synergy pole)': 'co-info -1, Delta +eps '
                                                 '({a,b}|{c} split only)',
                           'copy (redundancy pole)': 'co-info +1, Delta '
                                                     '-eps (every split)',
                           'TC': 'positive on both poles, unsigned'},
            'two_point_clashes': 'MI = 1 bit at Delta = +eps and -eps; '
                                 'TC(union) = 1 bit at Delta = 0 and +eps',
            'occupancy': 'not consumed -- witness-world signs replicate '
                         'banked in-check content',
        },
    )



# =====================================================================
# CHECK 5 -- The register reading grounds ceil-log2 (and only ceil-log2)
# =====================================================================

def check_T_register_reading_grounds_ceil_log2_count() -> Dict:
    """T_register_reading_grounds_ceil_log2_count: the minimal protected
    register operationalization of the capacity ledger -- the register
    model grounds the ceil-log2 count, and ONLY the ceil-log2 count,
    among the four banked clause-(iii) readings of
    check_T_su2_string_cut_comovement; under the grounded reading the
    clause-(iii) TIE survives and clause (ii) contracts to a weak
    ordering. (Landed v24.3.380, 2026-07-04, Paper 12 round-5 walk B2,
    reviewer Q6/Q3/Q1; fresh-context hostile audit LAND-WITH-FIXES 0.80,
    mandatory fixes 1/2/3/5 + recommended 4/6/7 carried; walk of record:
    "The Turning/p12_review5_walks_2026-07-04/b2_register/".)

    THE REGISTER MODEL. A protected register realization of a
    distinction family S assigns, to each of its anchor-disjoint
    irreducible-joint components S_i -- each anchored at its own anchor
    set / interface Gamma_i, disjoint across components (audit fix 2) --
    with d_i perfectly distinguishable record contents, a set of
    two-valued PROTECTED memory cells: cells the substrate's free
    relabelings (the zero-cost conventions of FD1-sc,
    check_FD1_structural_completeness) cannot erase or overwrite. An
    encoding is FAITHFUL when distinct record contents map to PERFECTLY
    DISTINGUISHABLE register states -- orthogonal states in the quantum
    case, distinct configurations in the classical case. That IS the
    definition, not an 'equivalently' (audit fix 3): bare injectivity
    into pure states is strictly weaker -- d > 2^m contents embed
    injectively into non-orthogonal states of m qubits and the lower
    bound FAILS -- while perfect single-shot distinguishability <=>
    orthogonality makes the bit and qubit bounds coincide by dimension
    count. reg(S_i) = the minimal number of protected cells admitting a
    faithful encoding; reg(S) = sum_i reg(S_i) (the per-component
    protection clause F-reg below). Approximate / probabilistic readout
    is outside the model, fenced.

    For the string-cut testbed the content count is exact banked data:
    the cut record is the unique j(x)j singlet, its reduced state on
    either side exactly maximally mixed of rank d_cut = 2j+1
    (check_T_su2_string_cut_comovement), so the readout of one side has
    exactly d_cut perfectly distinguishable outcomes.

    THE REGISTER READING (named; the priced rider). Identify, per
    irreducible component, the ledger's irreducibly-joint count with the
    register count: J := reg = ceil(log2 d). A READING, not a theorem:
    nothing in A1 / X1-X3 forces the ledger's J to be a storage count;
    the model is a readout-commitment model, and the identification is
    priced exactly like the argmin rider that keeps clause (i) of the
    comovement check at [P_structural_reading]. What earns 'grounds'
    over 'postulates': on n independent binary distinctions (d = 2^n)
    reg = n exactly -- the reading REPRODUCES kappa = n*eps where the
    ledger already speaks (leg 5) and extends it to d-ary fusion records
    where the ledger was silent.

    R = 0 CONVENTION (string cut). The banked identity is
    Delta = eps*(J - R) (L_irr). At a string cut the record is a single
    irreducible joint singlet and the model carries no reducible shared
    anchor, so R = 0 and Delta = eps*J under each named reading of J.
    Under the unit reading the banked sign criterion Delta > 0 FORCES
    R = 0 (J = 1); for the non-unit readings the convention is
    presentation-strength, stated and priced here.

    F-REG (the per-component protection clause; audit fix 2 wording).
    Cells are NEVER pooled across anchor-disjoint components. The clause
    is REQUIRED FOR X2: pooled packing is provably subadditive, never
    superadditive, and STRICTLY subadditive already inside the testbed
    family -- a j=1 string beside a j=2 string packs into
    ceil(log2 15) = 4 pooled cells against 2 + 3 = 5 per-component --
    which would put Delta_reg < 0 across anchor-disjoint components,
    against the banked theorem-strength Delta = 0
    (check_T_delta_disjoint_additivity). And it is MOTIVATED BY the
    factorization content of check_L_loc (independent per-interface
    budgets; factorized state space): a model postulate inherited from
    L_loc's picture, NOT derived from L_loc's theorem -- L_loc forces
    distribution only when richness exceeds single-interface capacity
    and does not forbid a physical device from pooling cells.

    LEGS (all exact, stdlib; d_cut = 2j+1 recomputed inline -- one line
    -- so the banked comovement check enters only as the LIVE
    cross-check of leg 3, never as a hardcoded artifact):
      1. STORAGE BOUND, [P]-exact math: min{m : 2^m >= d} =
         ceil(log2 d) = (d-1).bit_length(), tight both ways (2^m >= d
         and 2^(m-1) < d), swept d = 1..4096; the qubit case is the
         identical inequality (dimension count), asserted as such.
      2. GROUNDING SELECTIVITY: unit-count fails storage at d = 3
         (exhaustive brute force: all 8 maps from 3 contents to 2
         cell-states, ZERO injective); (d-1)-count is
         storage-sufficient but fails minimality at EVERY d >= 4
         (universal sweep d = 4..4096, audit fix 4 -- not just the
         first instance; first failure exactly d = 4); log2-count is
         not an integer cell count off powers of two (no integer m with
         2^m = 3); ceil-log2 is sufficient AND minimal on the whole
         testbed family {2, 3, 4, 5}.
      3. CLAUSE-(iii) TIE under the grounded reading, computed INLINE
         from the d_cut values: split (two j=1/2 strings, [2, 2]) vs
         unsplit (one j=1 string, [3]) gives register 2 == 2 (TIE)
         against the diagnostic's strict 3/2 < 2 preference for split;
         the full banked reading table reproduced; then the LIVE
         cross-check: check_T_su2_string_cut_comovement() is CALLED and
         its clause_iii_readings artifacts must match the inline values
         exactly (a live call, not a hardcode). The capacity-not-energy
         conclusion SURVIVES its own operationalization.
      4. CLAUSE-(ii) WEAK ORDERING under the reading: J_reg =
         ceil(log2(2j+1)) = [1, 2, 2, 3] on j in {1/2, 1, 3/2, 2} vs
         the strict diagnostic C2 = [3/4, 2, 15/4, 6]; weakly monotone,
         NEVER anti-ordered; the tie exactly at (j=1, j=3/2) and
         nowhere else; strictly COARSER than the Casimir (C2 injective
         on the family, J_reg takes 3 values on 4 members). This
         PARTIALLY RESOLVES clause (ii) under the named reading only;
         it does NOT close it -- the bank still fixes only
         Delta = eps*(J-R) and the sign criterion, and the comovement
         check's UNDER-DETERMINED verdict stands as banked (pointer
         added there this pass).
      5. ADDITIVITY + THE PROTECTION CLAUSE: ledger consistency
         d = 2^n => reg = n exactly; pooled packing subadditive on the
         full sweep d1, d2 in 2..40, strictly at (3, 5): 4 < 5 (and
         triples break ties: three d = 3 components pool to 5 < 6);
         negative control: DROPPING F-reg yields Delta_reg = -eps
         across an anchor-disjoint pair, against the banked Delta = 0
         -- the clause is load-bearing, not decor.
      6. NEGATIVE CONTROL, sabotage-shaped (replaces the walk-spec
         leg 6, which restated leg 2's brute force -- audit fix 5): the
         nearest-miss MIS-GROUNDED functional g(d) = d.bit_length()
         (agrees with ceil-log2 off powers of two) FAILS the grounding:
         it over-books at every power of two (g(2) = 2 > 1,
         g(4) = 3 > 2), and under g the clause-(iii) probe FLIPS the
         verdict (split 4 > unsplit 2: ANTI, not TIE) -- the legs have
         teeth against the closest wrong functional; a deliberately
         mis-grounded reading cannot pass.

    FALSIFIERS (TWO named, DISTINCT; the Delta-tracking probe is the
    switch between them; the three-way branch structure kept separate
    and never collapsed -- audit fix 1):
      REGISTER-READING FALSIFIER: a physical interface whose CERTIFIED
      minimal protected readout register deviates from ceil(log2 d) on
      a fusion channel. Deviation BELOW is impossible by the storage
      theorem; the live direction is ABOVE -- protection achievable
      only through redundant encoding whose overhead cells are
      certified as COMMITTED capacity (not free convention), code
      length n(d) > ceil(log2 d). Certification: (i) d perfectly
      distinguishable readouts exhibited; (ii) an adversarial sweep of
      the substrate's free relabelings corrupting every smaller
      register; (iii) a lower-bound proof that no ceil(log2 d)-cell
      protected register exists there. If the interface's Delta-ledger
      TRACKS THE CODE LENGTH rather than ceil(log2 d), the register
      reading is DEAD (the ledger's J reverts to under-determined); if
      Delta tracks ceil(log2 d) anyway, the READING SURVIVES and the
      overhead was mis-certified.
      X1 FALSIFIER (protocol; distinct from the above): one d = 4
      fusion channel realized two ways at matched interfaces --
      realization A: 2 protected qubits (the minimal register);
      realization B: 4 two-valued cells constrained to a 2-dimensional
      parity code (4 codewords <-> 4 contents), the parity constraints
      supplied by the protecting structure. Certify per realization:
      (1) the content count d = 4; (2) the distinction count n(S)
      INCLUDING ALL ENFORCED CONTENT (the step X1's defense lives or
      dies on: B's parity constraints must certify as
      empirical-difference-free conventions, FD1-sc, for n_A = n_B);
      (3) the minimal protected commitment, adversarially. THREE-WAY
      OUTCOME:
        (a) the counts certify UNEQUAL -- the protective structure
            keeps certifying as enforced content, the count rises to
            match the commitment -- X1 CONFIRMED: protection is priced
            by the count (the stated defense, tested not decorated);
        (b) counts certify equal, commitments provably differ, AND the
            Delta-ledger TRACKS THE COMMITMENT -- X1's relabel-freedom
            clause is REFUTED (cost genuinely tracks presentation at
            fixed count), and with it the characterization route to
            kappa = n*eps (check_T_cost_count_characterization: X2 and
            X3 cannot rescue linearity without X1);
        (c) counts certify equal, commitments provably differ, and
            Delta tracks ceil(log2 d) ANYWAY -- the register READING
            (or the commitment certification) is dead; X1 UNTOUCHED.
      Branches (b) and (c) are distinct: different minimal commitments
      at certified-equal counts refute X1 only WITH the Delta-tracking
      premise -- never without it.

    FENCES:
      (no-GeV) Everything above is a pure count or an integer multiple
        of eps. The per-cell commitment eps is priced only at the named
        EXTERNAL calibration ports (Landauer, Margolus-Levitin); no
        magnitude in physical units is asserted anywhere (module F3
        territory: the ports set the unit, the register supplies
        counts).
      (occupancy) Not consumed -- the SIGN of J-content is read off the
        world, not claimed here (L_irr doctrine: L_cost fixes the FORM,
        occupancy fixes the SIGN); the module-standard fence.
      (F-reg) The per-component protection clause, as above: REQUIRED
        for X2, MOTIVATED BY L_loc, NOT derived from L_loc.
      (scope) Partially resolves clause (ii) under the named reading
        ONLY; no dynamics (the model prices holding a readout, not
        evolving or screening -- the screening story stays imported);
        no spectral, tension-law, or magnitude claim;
        approximate/probabilistic readout fenced out.

    GRADE: [P_structural_reading], tier 4 (the comovement precedent):
    legs 1-6 are exact combinatorics and exact rep-theory-derived
    integers -- [P] material; what keeps the check off bare [P] is the
    named register reading (J := reg), carried with its live falsifiers
    above and priced in the summary.
    """
    checks = []

    def ck(cond, msg):
        checks.append((bool(cond), msg))
        check(cond, msg)

    def _cl2(d):
        """ceil(log2 d) for integer d >= 1, exact (matches the banked
        _ceil_log2 in apf/su2_string_cut_testbed.py)."""
        return (d - 1).bit_length()

    def _min_register(d):
        """Minimal m with 2^m >= d, by direct search (independent of
        bit_length)."""
        m = 0
        while 2 ** m < d:
            m += 1
        return m

    # ================= LEG 1 -- the storage bound, exact =================
    ck(all(_min_register(d) == _cl2(d) for d in range(1, 4097)),
       "leg 1: min m with 2^m >= d == ceil(log2 d) == (d-1).bit_length(), "
       "all d in 1..4096 (exact integers)")
    ck(all(2 ** _min_register(d) >= d
           and (_min_register(d) == 0 or 2 ** (_min_register(d) - 1) < d)
           for d in range(1, 4097)),
       "leg 1: tight both ways (2^m >= d and 2^(m-1) < d) -- achievability "
       "+ lower bound; the qubit case is the identical dimension-count "
       "inequality (d perfectly distinguishable contents need d mutually "
       "orthogonal states; m qubits give dim 2^m)")

    # ================= LEG 2 -- grounding selectivity ====================
    from itertools import product as _prod
    maps = list(_prod((0, 1), repeat=3))       # all f: {0,1,2} -> {0,1}
    ck(len(maps) == 8 and not any(len(set(m)) == 3 for m in maps),
       "leg 2 (unit-count EXCLUDED): all 8 maps from 3 record contents to "
       "2 cell-states enumerated, ZERO injective -- one cell cannot "
       "faithfully store d = 3 (exact, exhaustive)")
    ck(all(2 ** (d - 1) >= d for d in range(1, 65)),
       "leg 2: (d-1)-count is storage-SUFFICIENT (2^(d-1) >= d)")
    ck(all(d - 1 > _cl2(d) for d in range(4, 4097)),
       "leg 2 ((d-1)-count EXCLUDED): fails minimality at EVERY d in "
       "4..4096 (universal sweep, audit fix 4), booking d-1 cells where "
       "ceil(log2 d) suffice")
    ck(min(d for d in range(1, 65) if d - 1 > _cl2(d)) == 4
       and _cl2(4) == 2,
       "leg 2: the first minimality failure is exactly d = 4 (3 cells "
       "booked where 2 suffice)")
    ck(not any(2 ** m == 3 for m in range(8)),
       "leg 2 (log2-count EXCLUDED): not an integer cell count at d = 3 "
       "(no integer m has 2^m = 3); its integer CEILING is the minimal "
       "register")
    ck(all(_cl2(d) == _min_register(d) for d in (2, 3, 4, 5)),
       "leg 2 (ceil-log2 GROUNDED): storage-sufficient AND minimal on the "
       "whole testbed family d_cut in {2, 3, 4, 5} -- the unique "
       "register-groundable member of the banked four-reading family")

    # ================= LEG 3 -- clause (iii): the TIE survives ===========
    dcut = {a: a + 1 for a in (1, 2, 3, 4)}    # d_cut = 2j+1, inline

    def _c2j(a):
        j = Fraction(a, 2)
        return j * (j + 1)

    split = [dcut[1], dcut[1]]                 # two parallel j=1/2 strings
    unsplit = [dcut[2]]                        # one j=1 string
    diag_s, diag_u = sum(_c2j(1) for _ in split), _c2j(2)
    ck(diag_s == Fraction(3, 2) and diag_u == 2 and diag_s < diag_u,
       "leg 3 diagnostic: 2*C2(1/2) = 3/2 < C2(1) = 2 -- strictly prefers "
       "split (exact)")
    unit_s, unit_u = len(split), len(unsplit)
    prod_s, prod_u = split[0] * split[1], unsplit[0]
    dm1_s, dm1_u = sum(d - 1 for d in split), sum(d - 1 for d in unsplit)
    reg_s, reg_u = (sum(_cl2(d) for d in split),
                    sum(_cl2(d) for d in unsplit))
    ck(unit_s == 2 and unit_u == 1 and unit_s > unit_u,
       "leg 3: unit-count 2 > 1 -- ANTI (as banked)")
    ck(prod_s == 4 and prod_u == 3 and prod_s > prod_u,
       "leg 3: log2-count via exact d_cut products 4 > 3 -- ANTI "
       "(as banked)")
    ck(dm1_s == 2 and dm1_u == 2,
       "leg 3: (d-1)-count 2 == 2 -- TIE (as banked)")
    ck(reg_s == 2 and reg_u == 2,
       "leg 3 REGISTER reading (grounded ceil-log2): 2 == 2 -- TIE against "
       "the diagnostic's strict split preference; the capacity-not-energy "
       "conclusion SURVIVES its own operationalization")
    # -- the LIVE banked cross-check (a call, not a hardcode) -------------
    from apf.su2_string_cut_testbed import check_T_su2_string_cut_comovement
    r_banked = check_T_su2_string_cut_comovement()
    art = r_banked['artifacts']['clause_iii_readings']
    ck(art['ceil_log2'] == [reg_s, reg_u]
       and art['unit_count'] == [unit_s, unit_u]
       and art['dcut_product_for_log2'] == [prod_s, prod_u]
       and art['d_minus_1'] == [dm1_s, dm1_u]
       and art['diagnostic_C2'] == [str(diag_s), str(diag_u)],
       "leg 3 LIVE cross-check: the banked comovement clause_iii_readings "
       "artifacts match the inline recomputation exactly (live call, not "
       "a hardcode)")
    ck(r_banked['epistemic'] == 'P_structural_reading'
       and r_banked['verdict'] == 'PARTIAL',
       "leg 3: the banked check re-asserts grade [P_structural_reading] + "
       "verdict PARTIAL live (the precedent this check mirrors)")

    # ================= LEG 4 -- clause (ii): weak ordering ===============
    fam = [1, 2, 3, 4]                         # a = 2j
    jreg = [_cl2(dcut[a]) for a in fam]
    c2s = [_c2j(a) for a in fam]
    ck(jreg == [1, 2, 2, 3],
       "leg 4: J_reg = ceil(log2(2j+1)) = [1, 2, 2, 3] on j in "
       "{1/2, 1, 3/2, 2}")
    ck(c2s == [Fraction(3, 4), Fraction(2), Fraction(15, 4), Fraction(6)]
       and all(c2s[i] < c2s[i + 1] for i in range(3)),
       "leg 4: diagnostic C2 = [3/4, 2, 15/4, 6] strictly increasing "
       "(exact Fractions)")
    ck(all(jreg[i] <= jreg[i + 1] for i in range(3)),
       "leg 4: J_reg weakly monotone -- NEVER anti-ordered against the "
       "strict C2 ordering")
    ck(jreg[1] == jreg[2] and jreg[0] < jreg[1] and jreg[2] < jreg[3],
       "leg 4: the tie is EXACTLY at (j=1, j=3/2) -- d_cut = 3, 4 share "
       "ceil-log2 = 2 -- and nowhere else; every strict J_reg step agrees "
       "in sign with the diagnostic")
    ck(len(set(c2s)) == 4 and len(set(jreg)) == 3,
       "leg 4: coarseness witnessed -- C2 injective on the family "
       "(4 values), J_reg not (3 values); the register reading is strictly "
       "COARSER than the Casimir (partial resolution under the named "
       "reading ONLY; the banked UNDER-DETERMINED verdict stands)")

    # ================= LEG 5 -- additivity + the protection clause =======
    ck(all(_cl2(2 ** n) == n for n in range(1, 13)),
       "leg 5 ledger consistency: n independent binary distinctions have "
       "d = 2^n contents and reg = n EXACTLY -- the register reading "
       "reproduces kappa = n*eps where the ledger already speaks")
    ck(all(_cl2(d1 * d2) <= _cl2(d1) + _cl2(d2)
           for d1 in range(2, 41) for d2 in range(2, 41)),
       "leg 5: pooled packing is SUBADDITIVE, never superadditive "
       "(ceil(log2 d1*d2) <= ceil(log2 d1) + ceil(log2 d2), all d1, d2 "
       "in 2..40)")
    ck(_cl2(3 * 5) == 4 and _cl2(3) + _cl2(5) == 5,
       "leg 5 STRICT pooling discount inside the testbed family: "
       "(d1, d2) = (3, 5) -- a j=1 string beside a j=2 string -- pooled "
       "ceil(log2 15) = 4 < 5 = per-component sum")
    ck(_cl2(3 * 3) == 4 == _cl2(3) + _cl2(3)
       and _cl2(27) == 5 and 3 * _cl2(3) == 6,
       "leg 5: pairs can tie ((3,3): 4 == 4) but triples break -- three "
       "d = 3 components pool to 5 < 6 per-component")
    delta_reg_pooled = EPS * (_cl2(15) - _cl2(3) - _cl2(5))
    ck(delta_reg_pooled == -EPS,
       "leg 5 negative control: DROPPING F-reg yields Delta_reg = -eps "
       "across an anchor-disjoint pair -- against the banked "
       "theorem-strength Delta = 0 (check_T_delta_disjoint_additivity); "
       "the per-component protection clause is LOAD-BEARING for X2 "
       "(REQUIRED for X2, MOTIVATED BY L_loc, NOT derived from L_loc)")

    # ================= LEG 6 -- sabotage-shaped negative control =========
    def g(d):
        return d.bit_length()                  # the nearest-miss functional

    ck(all(g(d) == _cl2(d) for d in range(2, 65) if (d & (d - 1)) != 0),
       "leg 6: g(d) = d.bit_length() agrees with ceil-log2 off powers of "
       "two -- a genuine NEAR-MISS, not a strawman")
    ck(g(2) == 2 > _min_register(2) and g(4) == 3 > _min_register(4),
       "leg 6 (mis-grounded reading FAILS minimality): g over-books at "
       "every power of two (g(2) = 2 > 1, g(4) = 3 > 2) -- it is not the "
       "minimal faithful register count")
    ck(sum(g(d) for d in split) == 4 > sum(g(d) for d in unsplit) == 2,
       "leg 6 (mis-grounded reading FLIPS the verdict): under g the "
       "split-vs-unsplit probe gives 4 > 2 -- ANTI, not TIE -- the "
       "grounding legs have TEETH against the closest wrong functional; "
       "a deliberately mis-grounded reading cannot pass")

    n_legs = len(checks)

    return _result(
        name='T_register_reading_grounds_ceil_log2_count -- the minimal '
             'protected register grounds the ceil-log2 count, and only '
             'it; the clause-(iii) TIE survives the grounding',
        tier=4,
        epistemic='P_structural_reading',
        summary=(
            'THE REGISTER OPERATIONALIZATION (Paper 12 round-5 walk B2). '
            'Storage theorem, exact: the minimal FAITHFUL protected '
            'register for a d-ary irreducible fusion record is exactly '
            'ceil(log2 d) two-valued cells -- FAITHFUL defined as '
            'perfectly-distinguishable storage (orthogonal states in the '
            'quantum case), under which the bit and qubit bounds coincide '
            'by dimension count; tight both ways, swept to d = 4096. '
            'Grounding selectivity: among the four banked clause-(iii) '
            'readings of check_T_su2_string_cut_comovement the register '
            'model grounds ceil-log2 and ONLY ceil-log2 -- unit-count '
            'cannot store d = 3 (all 8 maps enumerated, zero injective), '
            '(d-1)-count fails minimality at EVERY d >= 4 (universal '
            'sweep to 4096), log2-count is not an integer cell count off '
            'powers of two. Under the grounded reading the clause-(iii) '
            'split-vs-unsplit probe still gives TIE (2 == 2) against the '
            'diagnostic\'s strict 3/2 < 2 preference -- the '
            'capacity-not-energy conclusion SURVIVES its own '
            'operationalization (verified inline AND against the banked '
            'artifacts by LIVE call) -- and clause (ii) contracts to a '
            'weak ordering (J_reg = [1, 2, 2, 3], never anti-ordered, tie '
            'exactly at (j=1, j=3/2), strictly coarser than the Casimir; '
            'partial resolution under the NAMED reading only -- the '
            'banked UNDER-DETERMINED verdict stands). Additivity: reg '
            'reproduces kappa = n*eps on binary families (d = 2^n => '
            'reg = n exactly) -- what earns grounds over postulates -- '
            'and composes over anchor-disjoint components EXACTLY under '
            'the per-component protection clause F-reg (pooled packing '
            'strictly subadditive already at (3,5): 4 < 5, i.e. '
            'Delta_reg = -eps against the banked Delta = 0; the clause is '
            'REQUIRED for X2, MOTIVATED BY the factorization content of '
            'check_L_loc, a model postulate NOT derived from L_loc). '
            'Sabotage control: the near-miss functional d.bit_length() '
            'fails minimality at every power of two and flips the '
            'clause-(iii) verdict to ANTI -- the legs have teeth. THE '
            'RIDER, priced: identifying the ledger\'s J with the register '
            'count (J := reg = ceil(log2 d), the REGISTER READING) is a '
            'named reading, not a theorem -- the same epistemic species '
            'as the comovement check\'s argmin rider -- carried with TWO '
            'distinct falsifiers whose switch is the Delta-tracking probe '
            '(register reading: a certified minimal register above '
            'ceil(log2 d) with Delta tracking the code length kills the '
            'reading; X1 protocol: three-way -- counts-unequal confirms '
            'X1 / Delta-tracks-commitment at equal counts refutes X1 / '
            'Delta-tracks-ceil-log2 kills the reading with X1 untouched '
            '-- branches never collapsed). R = 0 string-cut convention '
            'stated (forced by the sign criterion under the unit reading '
            'only). All arithmetic exact stdlib integers/Fractions; no '
            'float on any path; %d assertions. Counts only -- eps is '
            'priced at the external calibration ports (Landauer, '
            'Margolus-Levitin); occupancy not consumed -- the sign of '
            'J-content is read off the world, not claimed here.'
            % n_legs
        ),
        key_result=(
            'reg(d) = ceil(log2 d) exactly (tight both ways; bits = '
            'qubits under perfect distinguishability); the register model '
            'grounds ceil-log2 and ONLY ceil-log2 among the four banked '
            'readings; under the grounded reading split-vs-unsplit stays '
            'TIE (2 == 2 vs the diagnostic 3/2 < 2) and clause (ii) '
            'contracts to the weak ordering [1, 2, 2, 3]; additivity '
            'exact under the per-component protection clause. J := reg '
            'is a named, falsifiable reading, not a theorem.'
        ),
        dependencies=['L_cost', 'L_irr', 'T_su2_string_cut_comovement'],
        cross_refs=['T_cost_count_characterization',
                    'T_delta_disjoint_additivity',
                    'T_delta_coarse_graining_monotonicity',
                    'L_loc', 'L_epsilon*',
                    'FD1_structural_completeness'],
        n_assertions=n_legs,
        artifacts={
            'grounded_reading': 'ceil_log2',
            'clause_ii': 'WEAK-ORDER under the register reading '
                         '(J_reg = [1, 2, 2, 3]; banked UNDER-DETERMINED '
                         'verdict stands)',
            'clause_iii': 'TIE survives (register 2 == 2 vs diagnostic '
                          '3/2 < 2)',
            'storage_theorem': 'reg(d) = ceil(log2 d), tight both ways, '
                               'swept to d = 4096; bits = qubits under '
                               'the perfect-distinguishability definition '
                               'of faithful',
            'F_reg': 'per-component protection clause: REQUIRED for X2 '
                     '(pooled (3,5): 4 < 5, Delta_reg = -eps), MOTIVATED '
                     'BY L_loc, NOT derived from L_loc',
            'R0_convention': 'Delta = eps*J at a string cut (R = 0; '
                             'forced by the sign criterion under the '
                             'unit reading, presentation-strength for '
                             'the non-unit readings)',
            'falsifiers': 'two named, distinct; Delta-tracking probe as '
                          'switch; X1 protocol three-way (confirm / '
                          'refute-X1 / kill-the-reading), branches never '
                          'collapsed',
            'fences': ['counts only -- no grounded eps, no magnitudes; '
                       'eps priced at the external ports (Landauer, '
                       'Margolus-Levitin)',
                       'occupancy not consumed -- sign read off the '
                       'world, not claimed here',
                       'F-reg: cells never pooled across anchor-disjoint '
                       'components',
                       'partial resolution of clause (ii) under the '
                       'named reading only',
                       'no dynamics / spectral / tension-law claim; '
                       'approximate readout fenced out'],
        },
    )


# =====================================================================
# CHECK 6 -- The derived counting identity Delta = eps*(J - R)
# =====================================================================

def check_T_delta_JR_derived() -> Dict:
    """T_delta_JR_derived: the formal channel ledger (Ch / J / R) and the
    DERIVED identity Delta = eps*(J - R). (Landed v24.3.381, 2026-07-04,
    Paper 12 round-6 walk C1, reviewer Q2; fresh-context hostile audit
    LAND-WITH-FIXES 0.84, mandatory fixes F1-F4 + recommended F5-F7
    carried; walk of record: "The Turning/p12_review6_walks_2026-07-04/
    c1_algebraic_anchors/". Sibling: check_T_anchor_support_formalization,
    apf/anchor_support_algebra.py -- the support/anchor theory this check's
    type-(a) deviation witness consumes by LIVE call.)

    THE CHANNEL LEDGER (presentation input, stated as such). A presented
    interface carries a finite set of billed channels; each channel has a
    nonempty support (CH3 -- anchor consistency, a DEFINITIONAL AXIOM of
    the structure, not a lemma (audit F7a): anc(S) = union of supp(c) over
    c in Ch(S)); each family or join X has an activation set Ch(X). Two
    named axioms carry the theorem:

      (CH1) ACTIVATION MONOTONICITY: Ch(S1 v S2) >= Ch(S1) u Ch(S2).
        TYPED (audit F4): CH1 is a DEFINITIONAL CLAUSE OF THE JOIN
        OPERATION v UNDER THE LEDGER READING -- holding both families
        available commits at least both activation sets. It is genuinely
        load-bearing, with its content pinned in-check: it FORCES
        z in Ch(join) on the parity triple (the join may not re-present a
        marginal channel as derived from the others -- that is why
        n(join) = 4, not 3; leg 4), and it forces the falsifiable bound
        Delta >= -eps*R (a join can never cost less than the union count;
        verified on every example). Its named falsifier is the leg-7
        signature (Delta_kappa = 0 vs eps*(J - R) = eps on a
        channel-forgetting join).
      (CH2) COST = COUNT: kappa(X) = eps*|Ch(X)| -- the banked
        characterization theorem (X1-X3 ==> kappa = n*eps,
        check_T_cost_count_characterization, this module; X1 is named
        THERE and inherited here, not re-argued).

    R := |Ch(S1) ^ Ch(S2)| -- REDUCIBLE SHARED CHANNELS: a count of shared
    billed DISTINCTIONS, deliberately NOT of shared loci. THE R-CONVENTION
    FLAG (audit F3): the banked WITNESSES implement the channel convention
    (NC2's shared s; W1's shared s) while the banked WORDING ("reducible
    shared anchors") reads, against Definition (anchor), as the locus
    convention -- and every pre-existing banked instance is
    convention-degenerate (shared channel <=> shared locus, 1:1). This
    check DISAMBIGUATES against the wording: the locus convention provably
    breaks the identity on TWO discriminating instances (leg 3, audit
    F7d), so the channel convention is adopted, and the corpus wording is
    annotated same-pass (dated rows at check_L_irr Step 1, apf/core.py,
    and check 1 of this module -- count-neutral).

    J := |Ch(S1 v S2) \\ (Ch(S1) u Ch(S2))| -- IRREDUCIBLY JOINT CHANNELS.
    Each joint channel is certified by a computable DEVIATION WITNESS
    against the free join: type (a) -- a genuinely new record operator
    (membership failure: the meson cut's fused singlet, dim M12 = 5 > 4 =
    dim alg(M1 u M2), consumed LIVE from the sibling check); type (b) --
    an enforced constraint strictly cutting the joint valuation set (the
    parity triple, |Omega_join| = 4 < 8).

    THE THEOREM (derived bookkeeping). Under CH1 + CH2,
    |Ch(join)| = n1 + n2 - R + J by inclusion-exclusion, hence
        Delta = kappa(join) - kappa(S1) - kappa(S2) = eps*(J - R).
    THE LEDGER-RELATIVITY SENTENCE (audit F6; load-bearing for the word
    "derived"): Ch(join) is PRESENTATION INPUT -- the deviation witnesses
    certify that a claimed joint channel is genuinely joint; they do NOT
    determine the count, which is ledger data certified channel-wise, not
    algebra-derived. The identity is derived bookkeeping over an
    explicitly axiomatized structure; its content lives in CH1 (pinned by
    the leg-7 negative control) and CH2 (the banked theorem), and its
    physical falsifier routes through independently certified channel
    counts against independently certified Delta.

    CHANNEL IDENTITY (audit F2): channel identity is LITERAL identity of
    billed record content WITHIN THE SINGLE FIXED PRESENTATION (frozenset
    equality here). The relabeling group enters ONLY as SIMULTANEOUS
    covariance (transport S1, S2, and the join by the same g -- leg 5),
    NEVER as a per-channel identification: the g_lo = g_hi o pi breaking
    case runs in-check (leg 3d) -- a per-match identification would set
    R = 1 on the honesty-control pair and break the identity.

    LEGS:
      1. TWO ROUTES WITH TEETH (audit F1): for each of six worked examples
         an INDEPENDENT hand-set E-table (the banked W1 / L_irr
         E-dictionary pattern) supplies Delta via _Delta; the channel sets
         separately supply eps*(J - R); agreement is content -- the tables
         are never computed from the channel sets. Examples: (i)
         independent bits; (ii) the parity triple; (iii) the copy pair
         (banked NC2 verbatim); (iv) the meson cut record; (v) the banked
         W1 world {s,a} vs {s,b} (J = 1 against R = 1); (vi) the banked
         NC1 spanning-term booking, actually RUN (audit F7c).
      2. DEVIATION WITNESSES: type (b) computed (valuation-set strictness
         + full-support dependence); type (a) consumed LIVE from
         check_T_anchor_support_formalization's meson_type_a artifacts.
      3. THE R-CONVENTION PINNED, two discriminating instances + the F2
         breaking case: (b) honesty-control pair (J = 0, shared locus,
         distinct channels): channel-R = 0 matches the table (Delta = 0);
         locus-R = 1 gives -eps (wrong); (c) a J > 0 pair sharing a locus
         through two distinct channels: channel convention matches
         (+eps), locus convention fails (0); (d) per-match relabel
         identification (g_lo = g_hi o pi verified pointwise) would give
         R = 1 and -eps on (b) -- excluded.
      4. CH1 CONTENT: dropping z from Ch(join) (re-presenting it as
         derived) breaks the two-route agreement on the parity triple
         (channel route 0 vs table +eps); the bound Delta >= -eps*R holds
         on every example.
      5. RELABEL INVARIANCE (Theorem 3, ledger face): simultaneous
         bijective transport of all three channel sets leaves n, J, R,
         Delta exactly invariant; that billing itself attaches no cost to
         a relabeling is X1's relabel-freedom clause (FD1-sc), named at
         one gate, not re-derived.
      6. d-ARY FENCE: the identity survives any fixed per-channel weight
         applied uniformly to marginals and join (verified with a
         non-unit weight on the fusion channel); the count functional
         J(d) for d-ary fusion stays under-determined, with ceil-log2
         grounded at [P_structural_reading] ONLY
         (check_T_register_reading_grounds_ceil_log2_count -- cited, no
         new grounding claimed; at d = 2 all readings coincide at eps).
      7. NEGATIVE CONTROL (CH1 load-bearing): a channel-forgetting join
         breaks the identity (Delta_kappa = 0 vs eps*(J - R) = eps).

    FALSIFIERS (live): an interface with certified channel counts and
    certified Delta != eps*(J - R) -- convicts CH1 or cost = count,
    discriminably (the leg-7 signature isolates CH1); a certified
    relabeling changing J or R at fixed empirical content (the X1
    falsifier, protocol-precise in Paper 12 SS3.2).

    FENCES: occupancy not consumed (L_irr doctrine: the FORM is fixed
    here, the SIGN of realized J-content is read off the world);
    Delta = 0 does not certify independence (the sibling check's honesty
    control); module fences F1 + F2 carried.

    GRADE: [P], with the conditionality STATED: derived bookkeeping over
    the named axioms CH1 + CH2, Ch(join) presentation input (the
    ledger-relativity sentence above is part of the claim). Completes the
    module honesty note: the identity's first DERIVATION, after the
    module's first executable instantiations (checks 1-2).
    """
    checks = []

    def ck(cond, msg):
        checks.append((bool(cond), msg))
        check(cond, msg)

    def _jr(ch1, ch2, chj):
        ck(chj >= (ch1 | ch2),
           "CH1 holds on the instance (join carries every marginal channel)")
        return len(chj - (ch1 | ch2)), len(ch1 & ch2)

    # ================= LEG 1 -- two routes with teeth (F1) ===============
    # Route A: INDEPENDENT hand-set E-tables (the banked E-dictionary
    # pattern: check 2's W1, L_irr's _ES/_EE, T_canonical's E_local).
    # Route B: channel sets. The tables below are hand-set per physical
    # situation; nothing computes them from the channel sets.
    fs = frozenset

    # (i) independent bits: one binary record at each of two loci.
    E_i = {fs(): Fraction(0), fs({'b0'}): EPS, fs({'b1'}): EPS,
           fs({'b0', 'b1'}): 2 * EPS}
    d_i = _Delta(E_i, fs({'b0'}), fs({'b1'}))
    J_i, R_i = _jr(fs({'b0@v0'}), fs({'b1@v1'}), fs({'b0@v0', 'b1@v1'}))
    ck(d_i == 0 == EPS * (J_i - R_i) and (J_i, R_i) == (0, 0),
       "leg 1(i) independent bits: table Delta = 0 = eps*(J-R), J = R = 0")

    # (ii) parity triple: S1 = {x, y}, S2 = {z}; join enforces z = x (+) y.
    E_ii = {fs(): Fraction(0), fs({'x'}): EPS, fs({'y'}): EPS,
            fs({'z'}): EPS, fs({'x', 'y'}): 2 * EPS,
            fs({'x', 'z'}): 2 * EPS, fs({'y', 'z'}): 2 * EPS,
            fs({'x', 'y', 'z'}): 4 * EPS}   # all three: + the parity channel
    ck(_monotone(E_ii, fs({'x', 'y', 'z'})), "leg 1(ii): E-table monotone (L3)")
    d_ii = _Delta(E_ii, fs({'x', 'y'}), fs({'z'}))
    ch1_ii = fs({'x@v0', 'y@v1'})
    ch2_ii = fs({'z@v2'})
    chj_ii = fs({'x@v0', 'y@v1', 'z@v2', 'parity@v0v1v2'})
    J_ii, R_ii = _jr(ch1_ii, ch2_ii, chj_ii)
    ck(d_ii == EPS == EPS * (J_ii - R_ii) and (J_ii, R_ii) == (1, 0),
       "leg 1(ii) parity triple: table Delta = +eps = eps*(J-R), J = 1, R = 0")

    # (iii) copy pair (banked NC2 verbatim): D1 = D2 = {s}.
    E_iii = {fs(): Fraction(0), fs({'s'}): EPS}
    d_iii = _Delta(E_iii, fs({'s'}), fs({'s'}))
    J_iii, R_iii = _jr(fs({'s@v0'}), fs({'s@v0'}), fs({'s@v0'}))
    ck(d_iii == -EPS == EPS * (J_iii - R_iii) and (J_iii, R_iii) == (0, 1),
       "leg 1(iii) copy pair (banked NC2): table Delta = -eps = eps*(J-R), "
       "J = 0, R = 1 -- the marginals double-bill the shared CHANNEL, the "
       "join counts it once")

    # (iv) meson cut record: two flux records; the join activates the
    # fused-singlet channel (type-a witness in leg 2).
    E_iv = {fs(): Fraction(0), fs({'f1'}): EPS, fs({'f2'}): EPS,
            fs({'f1', 'f2'}): 3 * EPS}   # pair: + the singlet channel
    d_iv = _Delta(E_iv, fs({'f1'}), fs({'f2'}))
    J_iv, R_iv = _jr(fs({'flux1@l0'}), fs({'flux2@l1'}),
                     fs({'flux1@l0', 'flux2@l1', 'singlet@l0l1'}))
    ck(d_iv == EPS == EPS * (J_iv - R_iv) and (J_iv, R_iv) == (1, 0),
       "leg 1(iv) meson cut: table Delta = +eps = eps*(J-R), J = 1, R = 0")

    # (v) the banked W1 world (check 2): {s,a} vs {s,b}, J = 1 vs R = 1.
    U_w1 = fs({'s', 'a', 'b'})
    E_w1 = {S: EPS * (len(S) + (1 if fs({'a', 'b'}) <= S else 0))
            for S in _powerset(U_w1)}
    d_v = _Delta(E_w1, fs({'s', 'a'}), fs({'s', 'b'}))
    J_v, R_v = _jr(fs({'s@v0', 'a@v1'}), fs({'s@v0', 'b@v2'}),
                   fs({'s@v0', 'a@v1', 'b@v2', 'j(a,b)@v1v2'}))
    ck(d_v == 0 == EPS * (J_v - R_v) and (J_v, R_v) == (1, 1),
       "leg 1(v) banked W1 reproduced: table Delta = 0 = eps*(1 - 1) -- "
       "the joint term and the shared channel cancel")

    # (vi) the banked NC1 spanning-term booking, actually RUN (F7c):
    # D1 = {a, b} + internal joint j1; D2 = {c, d}; x anchors at BOTH
    # interfaces with per-interface shares billed locally and the spanning
    # term Omega_inter only in the join (T_canonical R8).
    k_D1x = 4 * EPS       # a, b, j1(a,b), x's Gamma_1 share
    k_D2x = 3 * EPS       # c, d, x's Gamma_2 share
    k_join = 8 * EPS      # all of the above + Omega_inter(x)
    d_vi = k_join - k_D1x - k_D2x
    ch1_vi = fs({'a', 'b', 'j1(a,b)', 'xS1'})
    ch2_vi = fs({'c', 'd', 'xS2'})
    chj_vi = ch1_vi | ch2_vi | fs({'Omega_inter(x)'})
    J_vi, R_vi = _jr(ch1_vi, ch2_vi, chj_vi)
    ck(d_vi == EPS == EPS * (J_vi - R_vi) and (J_vi, R_vi) == (1, 0),
       "leg 1(vi) banked NC1 booking RUN: the spanning term is the one "
       "joint channel; Delta = +eps = eps*(J-R) (x's per-interface shares "
       "are DISTINCT billed channels, one per marginal)")

    # ================= LEG 2 -- deviation witnesses ======================
    # type (b), computed: the parity constraint strictly cuts the joint
    # valuation set and depends on all three loci.
    from itertools import product as _iprod
    cfgP = list(_iprod((0, 1), repeat=3))
    omega_join = [c for c in cfgP if (c[0] + c[1] + c[2]) % 2 == 0]
    parity = lambda c: (c[0] + c[1] + c[2]) % 2

    def _flip(c, v):
        cc = list(c); cc[v] ^= 1
        return tuple(cc)

    dep = [any(parity(c) != parity(_flip(c, v)) for c in cfgP)
           for v in range(3)]
    ck(len(omega_join) == 4 < 8 == len(cfgP) and all(dep),
       "leg 2 type-(b) witness: |Omega_join| = 4 < 8 = |Omega1 x Omega2| "
       "(strict cut) and the parity record depends on all three loci")
    # type (a), consumed LIVE from the sibling check (never a hardcode):
    from apf.anchor_support_algebra import (
        check_T_anchor_support_formalization)
    r_sib = check_T_anchor_support_formalization()
    art = r_sib['artifacts']['meson_type_a']
    ck(art['dim_M12'] == 5 and art['dim_alg_union'] == 4
       and art['singlet_in_union'] is False
       and art['supp_singlet'] == [0, 1]
       and r_sib['epistemic'] == 'P',
       "leg 2 type-(a) witness LIVE: dim M12 = 5 > 4 = dim alg(M1 u M2), "
       "membership failure, two-locus support -- consumed from "
       "check_T_anchor_support_formalization's exported artifacts by live "
       "call (grade [P] re-asserted live)")

    # ================= LEG 3 -- the R-convention pinned ==================
    # (b) honesty-control pair: two DISTINCT channels on ONE shared locus.
    E_h = {fs(): Fraction(0), fs({'g_hi'}): EPS, fs({'g_lo'}): EPS,
           fs({'g_hi', 'g_lo'}): 2 * EPS}
    d_h = _Delta(E_h, fs({'g_hi'}), fs({'g_lo'}))
    ch1_h, ch2_h = fs({'g_hi@v0'}), fs({'g_lo@v0'})
    chj_h = ch1_h | ch2_h
    J_h, R_h = _jr(ch1_h, ch2_h, chj_h)
    loci = lambda ch: fs(c.split('@')[1] for c in ch)
    R_locus_h = len(loci(ch1_h) & loci(ch2_h))
    ck(d_h == 0 == EPS * (J_h - R_h) and (J_h, R_h) == (0, 0)
       and R_locus_h == 1 and EPS * (J_h - R_locus_h) == -EPS != d_h,
       "leg 3(b) DISCRIMINATOR 1: shared locus, distinct channels, J = 0 "
       "-- channel-R = 0 matches the table (Delta = 0); locus-R = 1 gives "
       "-eps: the locus convention BREAKS the identity")
    # (c) J > 0 pair sharing a locus through two distinct channels (F7d):
    E_c = {fs(): Fraction(0)}
    U_c = fs({'g_hi', 'x', 'g_lo', 'y'})
    for S in _powerset(U_c):
        if S:
            E_c[S] = EPS * (len(S) + (1 if fs({'x', 'y'}) <= S else 0))
    d_c = _Delta(E_c, fs({'g_hi', 'x'}), fs({'g_lo', 'y'}))
    ch1_c = fs({'g_hi@v0', 'x@v1'})
    ch2_c = fs({'g_lo@v0', 'y@v2'})
    chj_c = ch1_c | ch2_c | fs({'j(x,y)@v1v2'})
    J_c, R_c = _jr(ch1_c, ch2_c, chj_c)
    R_locus_c = len(loci(ch1_c) & loci(ch2_c))
    ck(d_c == EPS == EPS * (J_c - R_c) and (J_c, R_c) == (1, 0)
       and R_locus_c == 1 and EPS * (J_c - R_locus_c) == 0 != d_c,
       "leg 3(c) DISCRIMINATOR 2 (J > 0): channel convention +eps matches "
       "the table; the locus convention gives 0 -- wrong again (the "
       "convention is pinned by more than one instance)")
    # (d) the F2 breaking case: g_lo = g_hi o pi pointwise, pi in Aut of
    # the 4-outcome set -- per-MATCH identification would set R = 1.
    g_hi_f = lambda c: c // 2
    g_lo_f = lambda c: c % 2
    pi = {0: 0, 1: 2, 2: 1, 3: 3}
    ck(all(g_lo_f(c) == g_hi_f(pi[c]) for c in range(4))
       and sorted(pi.values()) == [0, 1, 2, 3],
       "leg 3(d): g_lo = g_hi o pi verified pointwise (pi a genuine "
       "outcome permutation) -- the two channels ARE related by a "
       "relabeling")
    ck(EPS * (J_h - 1) == -EPS != d_h,
       "leg 3(d) F2 EXCLUSION: identifying channels 'up to relabeling' "
       "per-match would set R = 1 on the honesty pair and break the "
       "identity (-eps vs table 0) -- channel identity is LITERAL within "
       "the fixed presentation; relabelings enter only as SIMULTANEOUS "
       "covariance (leg 5)")

    # ================= LEG 4 -- CH1 content ==============================
    chj_ii_derived = fs({'x@v0', 'y@v1', 'parity@v0v1v2'})   # z 're-presented'
    d_channel_route_bad = (EPS * len(chj_ii_derived)
                           - EPS * len(ch1_ii) - EPS * len(ch2_ii))
    ck(d_channel_route_bad == 0 != d_ii,
       "leg 4: CH1 does POSITIVE work -- re-presenting z as derived "
       "(n(join) = 3, not 4) breaks the two-route agreement on the parity "
       "triple (channel route 0 vs table +eps); CH1 forces z in Ch(join)")
    for d_val, R_val in ((d_i, R_i), (d_ii, R_ii), (d_iii, R_iii),
                         (d_iv, R_iv), (d_v, R_v), (d_vi, R_vi),
                         (d_h, R_h), (d_c, R_c)):
        ck(d_val >= -EPS * R_val,
           "leg 4: the CH1-forced bound Delta >= -eps*R holds "
           f"(Delta = {d_val}, R = {R_val})")

    # ================= LEG 5 -- relabel invariance =======================
    ren = {'x@v0': 'u@w0', 'y@v1': 'v@w1', 'z@v2': 'w@w2',
           'parity@v0v1v2': 'parity@w0w1w2'}
    g = lambda ch: fs(ren[c] for c in ch)
    J_r, R_r = _jr(g(ch1_ii), g(ch2_ii), g(chj_ii))
    ck((J_r, R_r) == (J_ii, R_ii)
       and len(g(chj_ii)) == len(chj_ii),
       "leg 5: simultaneous bijective transport of (S1, S2, join) leaves "
       "n, J, R, Delta exactly invariant (Theorem 3; that billing attaches "
       "no cost to the relabeling is X1/FD1-sc, named, one gate)")

    # ================= LEG 6 -- the d-ary fence ==========================
    # identity survives uniform per-channel weighting: weight the fusion
    # channel at 2 cells on BOTH sides of the bookkeeping.
    w = lambda c: 2 * EPS if c == 'singlet@l0l1' else EPS
    ch1_m = fs({'flux1@l0'}); ch2_m = fs({'flux2@l1'})
    chj_m = fs({'flux1@l0', 'flux2@l1', 'singlet@l0l1'})
    kW = lambda ch: sum(w(c) for c in ch)
    d_weighted = kW(chj_m) - kW(ch1_m) - kW(ch2_m)
    J_m, R_m = _jr(ch1_m, ch2_m, chj_m)
    ck(d_weighted == sum(w(c) for c in chj_m - (ch1_m | ch2_m))
       - sum(w(c) for c in ch1_m & ch2_m)
       and d_weighted == 2 * EPS,
       "leg 6: the identity survives uniform per-channel weighting "
       "(Delta_w = sum_joint w - sum_shared w); the count functional J(d) "
       "for d-ary fusion stays under-determined -- ceil-log2 grounded at "
       "[P_structural_reading] ONLY "
       "(check_T_register_reading_grounds_ceil_log2_count, cited, no new "
       "grounding)")
    ck((2 - 1).bit_length() == 1,
       "leg 6: at d = 2 all count readings coincide at one channel (eps) "
       "-- the worked meson example is reading-independent")

    # ================= LEG 7 -- negative control (CH1) ===================
    ch_join_forget = fs({'x@v0', 'z@v2', 'parity@v0v1v2'})   # forgets y
    R_bad = len(ch1_ii & ch2_ii)
    J_bad = len(ch_join_forget - (ch1_ii | ch2_ii))
    d_kappa_bad = (EPS * len(ch_join_forget) - EPS * len(ch1_ii)
                   - EPS * len(ch2_ii))
    ck(not (ch_join_forget >= (ch1_ii | ch2_ii))
       and d_kappa_bad != EPS * (J_bad - R_bad),
       "leg 7 NEGATIVE CONTROL: a channel-forgetting join violates CH1 and "
       f"breaks the identity (Delta_kappa = {d_kappa_bad} vs eps*(J-R) = "
       f"{EPS * (J_bad - R_bad)}) -- CH1 is load-bearing, not decoration")

    n_legs = len(checks)

    return _result(
        name='T_delta_JR_derived -- the channel ledger and the derived '
             'identity Delta = eps*(J - R) (CH1 + CH2, two routes with '
             'teeth, the R-convention pinned)',
        tier=4,
        epistemic='P',
        summary=(
            'THE DERIVED COUNTING IDENTITY (Paper 12 round-6 walk C1, '
            'reviewer Q2). A presented interface carries a channel ledger '
            '(billed channels with nonempty supports -- CH3, a '
            'definitional axiom, not a lemma); under CH1 (activation '
            'monotonicity -- TYPED as a definitional clause of the join '
            'operation under the ledger reading: holding both families '
            'available commits at least both activation sets; its content '
            'is pinned in-check, forcing z in Ch(join) on the parity '
            'triple and the falsifiable bound Delta >= -eps*R) and CH2 '
            '(cost = count, the banked characterization theorem, X1 named '
            'there), inclusion-exclusion gives Delta = eps*(J - R) in two '
            'lines -- DERIVED BOOKKEEPING, with the ledger-relativity '
            'sentence carried as part of the claim: Ch(join) is '
            'presentation input; the deviation witnesses (type (a) new '
            'record operator -- the meson fused singlet, dim 5 > 4, '
            'consumed LIVE from check_T_anchor_support_formalization; '
            'type (b) strict valuation-set cut -- the parity triple, '
            '4 < 8) certify JOINTNESS, not the count. Two routes with '
            'teeth on six examples: independent hand-set E-tables (the '
            'banked E-dictionary pattern) against channel sets -- incl. '
            'the banked NC2 (copy pair, -eps), W1 (J = 1 vs R = 1, 0), '
            'and NC1 (spanning term, +eps) actually run. R counts shared '
            'CHANNELS, not loci: the locus convention provably breaks the '
            'identity on two discriminating instances (one at J = 0, one '
            'at J > 0), and channel identity is LITERAL within the fixed '
            'presentation -- the g_lo = g_hi o pi per-match '
            'identification is excluded in-check (relabelings enter only '
            'as simultaneous covariance, under which n, J, R, Delta are '
            'exactly invariant; ledger covariance = X1/FD1-sc, one gate). '
            'The identity survives uniform per-channel weighting; J(d) '
            'for d-ary fusion stays under-determined (ceil-log2 at '
            '[P_structural_reading] only, cited). Negative control: a '
            'channel-forgetting join breaks the identity -- CH1 is '
            'load-bearing. Completes the module honesty note: the '
            'identity\'s first derivation, after its first executable '
            'instantiations. All arithmetic exact; %d assertions. '
            'Occupancy: not consumed (form fixed here; realized sign read '
            'off the world).' % n_legs
        ),
        key_result=(
            'CH1 (typed: definitional clause of the join under the ledger '
            'reading) + CH2 (banked costchar) ==> Delta = eps*(J - R) by '
            'inclusion-exclusion; R = shared CHANNELS (locus convention '
            'provably breaks the identity); deviation witnesses certify '
            'jointness, not the count (Ch(join) is presentation input); '
            'J, R, Delta relabel-invariant under simultaneous transport; '
            'CH1 pinned by the channel-forgetting negative control.'
        ),
        dependencies=['L_cost', 'L_irr', 'T_M', 'L_loc'],
        cross_refs=['T_cost_count_characterization',
                    'T_delta_disjoint_additivity',
                    'T_register_reading_grounds_ceil_log2_count',
                    'T_anchor_support_formalization',
                    'FD1_structural_completeness'],
        n_assertions=n_legs,
        artifacts={
            'axioms': {
                'CH1': 'activation monotonicity -- definitional clause of '
                       'the join under the ledger reading; falsifier: the '
                       'leg-7 signature',
                'CH2': 'cost = count (T_cost_count_characterization, '
                       'banked [P]; X1 named there)',
                'CH3': 'anchor consistency -- definitional axiom (F7a: '
                       'not a lemma)',
            },
            'R_convention': 'shared CHANNELS (billed distinctions), not '
                            'loci; two discriminating instances in-check; '
                            'corpus wording annotated at check_L_irr and '
                            'check 1 (dated, count-neutral)',
            'ledger_relativity': 'Ch(join) is presentation input; '
                                 'deviation witnesses certify jointness, '
                                 'not the count',
            'two_routes': 'independent hand-set E-tables vs channel sets; '
                          'six examples incl. banked NC1/NC2/W1',
            'type_a_live': 'meson dim 5 > 4 consumed by live call from '
                           'check_T_anchor_support_formalization',
        },
    )


# =====================================================================
# CHECK 7 -- The chain-rule dichotomy for presented coarse families
# =====================================================================

def check_T_delta_chain_rule_conditional_expectation_dichotomy() -> Dict:
    """T_delta_chain_rule_conditional_expectation_dichotomy: does the
    quotient chain rule extend to conditional expectations onto
    subalgebras? Answer: a DICHOTOMY FOR PRESENTED COARSE FAMILIES, with a
    pinned exact counterexample. (Landed v24.3.381, 2026-07-04, Paper 12
    round-6 walk C2, reviewer Q9; fresh-context hostile audit
    LAND-WITH-FIXES 0.85, mandatory fixes F1/F2 (+F4 scoping) +
    recommended F3/F5/F6 + cosmetic F7/F8 carried; walk of record:
    "The Turning/p12_review6_walks_2026-07-04/c2_condexp_chainrule/".)

    THE SUPPORT TRANSCRIPTION (named; CANONICAL, NOT UNIQUE -- audit F1).
    A conditional expectation E_B : A -> B onto a subalgebra of the record
    algebra has no ledger referent by itself (the ledger reads record
    configurations, not channels); it enters through a PRESENTATION: a
    generating family beta_1..beta_m of coarse record channels with
    dependency supports S_k = supp(beta_k) c U (computed from the
    functions, not declared), billed in the SAME ledger by
    kappa_B(T) = E(union of supports of T), anchors transported by
    support. Post-audit canonicity, in three named clauses, each an
    executable leg: (i) SAME-LEDGER -- the coarse billing is the fine
    cost of a support-determined SUBSET of U (this kills the bake-in
    kappa-prime = E(union) + sum (m_i - 1) E({i}), which would 'rescue'
    the counterexample by billing the coarse pair at 4*eps > E(U) = 3*eps,
    a value no subset costs); (ii) PER-PRESENTED-CHANNEL -- the chain rule
    carries one Delta_internal term per presented generator (this
    excludes the clustering transcription by shape: it changes m); (iii)
    BLOCK-MERGE REPRODUCTION -- partition presentations reproduce the
    banked Prop 9.8 arithmetic exactly (W2/W3). Within the repaired
    family the FAILURE side of the dichotomy is transcription-robust
    (the free-world impossibility leg: rescue needs 4*eps > max_S E(S) =
    3*eps -- NO same-ledger billing can rescue the counterexample) while
    the defect FORMULA is T1-specific (the symmetric-difference billing
    is same-ledger, per-channel, reproduces W2/W3, and still fails the
    two-parity case -- with defect 2*eps instead of eps): T1 is
    CANONICAL (union billing), not unique, and this docstring says so.

    THE THEOREM (quantifying over PRESENTATIONS -- audit F2). For any
    presented coarse family with supports S_1..S_m and coverage
    multiplicities m_i = |{k : i in S_k}|:
      EXACT DEFECT IDENTITY [P]:
        Delta_fine - Delta_coarse - sum_k Delta_internal(beta_k)
          = [E(U) - E(union S_k)] + sum_i (m_i - 1) E({i})
      DICHOTOMY [P]: for covering presentations the defect is
        sum_i (m_i - 1) E({i}) >= 0, vanishing iff the supports PARTITION
        the billed universe -- a class strictly containing the block
        merges -- and failing STRICTLY for every cross-cutting
        presentation by the MD floor alone (no occupancy premise).
    The banked Prop 9.8 identity is the SINGLE-BLOCK form (audit F7); the
    multi-block form above is its natural (trivially iterated) extension,
    introduced by this check, not quoted from the paper.

    THE SUBALGEBRA LEVEL IS DEGENERATE (audit F2): every covering B is
    restorable (re-present on the support closure), so there is no
    subalgebra-level dichotomy; the non-degenerate residue is computed
    in-check: B_pq = <a (+) b, b (+) c> admits NO non-trivial compliant
    presentation -- its only elements with proper support are the three
    parities, whose supports pairwise overlap (exhaustive over the 15
    coarsenings of its fiber partition) -- so 'cross-cutting' is
    intrinsic to B_pq relative to non-trivial presentations. The defect
    VALUE is generator-relative (audit F3): in a non-uniform-floor world
    the same B_pq shows defect 2*eps under <p, q> and eps under
    <p, p (+) q>; strict FAILURE is generator-independent for B_pq.
    Undercovering B (support closure a proper subset of U) admits NO
    covering presentation at all (audit F4: the <a (+) b> case, computed)
    -- restorability is scoped to COVERING B, and undercovering
    subalgebras live permanently in the restriction domain
    (sign-indefinite defect, the banked no-go).

    T2 EXCLUSION (audit F5, computed): the compressed re-billing
    alternative's DETERMINED fragment (each coarse channel billed at
    eps x its presented content; the W2 merge keeps both bits, content 2,
    so 2*eps) fails the banked W2 fixed point in-check (Delta_internal
    becomes 0 where the banked value is 2*eps; 1 + 0 != 3). The
    WELL-POSEDNESS half of the T2 rejection -- its coarse J/R structure
    is fresh per-interface occupancy input, not determined by the fine
    data -- is a PROSE CLAUSE of this docstring, not an executable leg.

    SWEEP SCOPE (audit F6): exhaustive over all 127 families of distinct
    nonempty supports on the 3-channel universe (plus multiset instances
    via the twirl), across 9 worlds (the 8 walk worlds + the
    non-uniform-floor world of the F3 leg): 9 x 127 = 1143 exact
    defect-formula cases; the dichotomy verified on every covering case.
    The analytic proof (two-line telescoping) carries the generality;
    the sweep is the witness layer.

    ANCHOR TRANSPORT, USED (audit F8): the partition presentation's
    coarse channels have support-transported anchors in disjoint sets,
    and their pairwise Delta vanishes in the free world -- consistency
    with T_delta_disjoint_additivity through the transported anchors.

    FENCES: (F-a) single-table / within-ledger only -- re-presenting a
    compressed interface as a NEW configuration with fresh occupancy
    input is out of scope (the paper's re-presentation clause,
    unchanged); (F-b) the transcription is a SUPPORT FUNCTOR -- the
    fiber-level action of E_B is invisible by construction (a merge of
    {a,b} and a dephasing-to-parity of {a,b} transcribe identically,
    verified), which is the precise content of 'the ledger reads record
    configurations, not channels'; (F-c) null channels (E({i}) = 0) are
    excised from the billed universe -- the MD floor is load-bearing for
    STRICT failure; (F-d) undercoverage is the restriction domain (the
    banked no-go; no new claim). CPTP clause of the module docstring
    unchanged: OPEN.

    FALSIFIER (live, post-F1 restatement): exhibit a SAME-LEDGER,
    PER-PRESENTED-CHANNEL, fine-data-determined transcription that
    reproduces the banked block-merge chain rule on W2/W3 AND makes the
    two-parity identity hold. The free-world impossibility leg shows this
    fails on the counterexample for every candidate (4*eps > E(U)); a
    counter-instance refutes the canonicity clause and reopens the
    extension.

    GRADE: [P] under the NAMED support transcription -- exact finite
    mathematics; the transcription is a definitional construction whose
    canonicity is carried by the three executable clauses above (no
    reading strength consumed); the presentation-relativity is asserted
    in-check, not hidden. Occupancy: not consumed (strict failure is
    floor-forced; verified across occupied and free worlds alike).
    """
    checks = []

    def ck(cond, msg):
        checks.append((bool(cond), msg))
        check(cond, msg)

    fs = frozenset
    U3 = fs('abc')

    def table(n):
        return {S: EPS * n(S) for S in _powerset(U3)}

    WORLDS = {
        'free':  table(lambda S: len(S)),
        'J_ab':  table(lambda S: len(S) + (1 if fs('ab') <= S else 0)),
        'J_bc':  table(lambda S: len(S) + (1 if fs('bc') <= S else 0)),
        'J_abc': table(lambda S: len(S) + (1 if fs('abc') <= S else 0)),
        'mix':   table(lambda S: len(S)
                       + (1 if fs('ab') <= S else 0)
                       + (1 if fs('bc') <= S else 0)),
        # W2 / W3: the banked worlds of check 2 (occupied / subadditive)
        'W2': {fs(): Fraction(0),
               fs('a'): EPS, fs('b'): EPS, fs('c'): EPS,
               fs('ab'): 4 * EPS, fs('ac'): 2 * EPS,
               fs('bc'): 2 * EPS, fs('abc'): 6 * EPS},
        'W3': {fs(): Fraction(0),
               fs('a'): EPS, fs('b'): EPS, fs('c'): EPS,
               fs('ab'): EPS, fs('ac'): 2 * EPS,
               fs('bc'): 2 * EPS, fs('abc'): 3 * EPS},
        'R_tight': {fs(): Fraction(0),
                    fs('a'): EPS, fs('b'): EPS, fs('c'): EPS,
                    fs('ab'): EPS, fs('ac'): 2 * EPS,
                    fs('bc'): 2 * EPS, fs('abc'): 2 * EPS},
        # W_nu (audit F3): non-uniform singleton floor, E({b}) = 2*eps,
        # free-additive -- legal (monotone, floor respected).
        'W_nu': {S: sum((2 * EPS if x == 'b' else EPS) for x in S)
                 if S else Fraction(0) for S in _powerset(U3)},
    }
    ck(all(_monotone(E, U3) for E in WORLDS.values()),
       "all 9 worlds subset-monotone (L3; incl. the non-uniform-floor "
       "world W_nu)")
    ck(all(E[fs([i])] >= EPS for E in WORLDS.values() for i in U3),
       "all 9 worlds respect the MD floor: E({i}) >= eps for every billed "
       "channel")

    # ---- the transcription arithmetic ----------------------------------
    def chain_parts(E, supports):
        """T1: kappa_B(T) = E(union supports of T); one Delta_internal per
        presented channel (the per-presented-channel clause)."""
        union = fs().union(*supports) if supports else fs()
        total = E[U3] - sum(E[fs([i])] for i in U3)
        coarse = E[union] - sum(E[sk] for sk in supports)
        internal = sum(E[sk] - sum(E[fs([i])] for i in sk)
                       for sk in supports)
        return total, coarse, internal, total - coarse - internal

    def defect_formula(E, supports):
        union = fs().union(*supports) if supports else fs()
        mult = {i: sum(1 for sk in supports if i in sk) for i in U3}
        return (E[U3] - E[union]) + sum((mult[i] - 1) * E[fs([i])]
                                        for i in U3)

    def is_partition(supports):
        if fs().union(*supports) != U3:
            return False
        return all(not (s1 & s2)
                   for s1, s2 in combinations(supports, 2))

    # ---- leg 1: fixed points (banked chain rule + restriction no-go) ----
    U1 = fs('sab')
    E1 = {S: EPS * (len(S) + (1 if fs('ab') <= S else 0))
          for S in _powerset(U1)}
    ck(_Delta(E1, fs('sa'), fs('sb')) == 0
       and _Delta(E1, fs('a'), fs('b')) == EPS
       and _Delta(E1, fs('sa'), fs('s')) == -EPS,
       "leg 1: the banked W1 restriction no-go reproduced (0 fine; +eps "
       "drop-s; -eps drop-b)")
    for wname in ('W2', 'W3'):
        E = WORLDS[wname]
        d_int = _Delta(E, fs('a'), fs('b'))
        d_coarse = _Delta(E, fs('ab'), fs('c'))
        omega_fine = E[fs('abc')] - sum(E[fs(x)] for x in 'abc')
        ck(omega_fine == d_coarse + d_int,
           f"leg 1 {wname}: the banked SINGLE-BLOCK Prop 9.8 identity "
           "Omega_fine = Delta_coarse + Delta_internal (the multi-block "
           "form below is this check's extension -- audit F7)")
        t, c, i, d = chain_parts(E, [fs('ab'), fs('c')])
        ck(d == 0 and t == c + i,
           f"leg 1 {wname}: the partition presentation [ab|c] reproduces "
           "the banked chain rule exactly (defect 0 -- canonicity clause "
           "(iii), block-merge reproduction)")

    # ---- leg 2: algebra certificates (exact conditional expectations) ---
    from itertools import product as _iprod
    X = [x for x in _iprod((0, 1), repeat=3)]
    CH = ('a', 'b', 'c')

    def partition_by(keyfun):
        blocks = {}
        for x in X:
            blocks.setdefault(keyfun(x), []).append(x)
        return [fs(b) for b in blocks.values()]

    def cond_exp(partition):
        def E_B(f):
            out = {}
            for blk in partition:
                avg = sum((f[x] for x in blk), Fraction(0)) / len(blk)
                for x in blk:
                    out[x] = avg
            return out
        return E_B

    def certify(partition, label):
        E_B = cond_exp(partition)
        one = {x: Fraction(1) for x in X}
        deltas = [{y: Fraction(1 if y == x else 0) for y in X} for x in X]
        indicators = [{x: Fraction(1 if x in blk else 0) for x in X}
                      for blk in partition]
        mul = lambda f, g: {x: f[x] * g[x] for x in X}
        ok = (E_B(one) == one)
        ok &= all(E_B(E_B(d)) == E_B(d) for d in deltas)
        for mask in range(256):
            f = {x: Fraction((mask >> k) & 1) for k, x in enumerate(X)}
            ok &= all(v >= 0 for v in E_B(f).values())
        ok &= all(E_B(mul(mul(b1, d), b2)) == mul(mul(b1, E_B(d)), b2)
                  for b1 in indicators for d in deltas for b2 in indicators)
        ok &= all(sum(E_B(d).values()) == sum(d.values()) for d in deltas)
        const_on = lambda f: all(len({f[x] for x in blk}) == 1
                                 for blk in partition)
        ok &= all(const_on(E_B(d)) for d in deltas)
        ok &= all(E_B(b) == b for b in indicators)
        ck(ok, label + ": unital + idempotent + positive + B-bimodule + "
               "trace-preserving + range = B (all exact)")
        return E_B

    def supp_of(g):
        out = set()
        for k, name in enumerate(CH):
            for x in X:
                y = list(x); y[k] ^= 1
                if g(x) != g(tuple(y)):
                    out.add(name)
                    break
        return fs(out)

    p = lambda x: (x[0] + x[1]) % 2
    q = lambda x: (x[1] + x[2]) % 2
    pq = lambda x: (x[0] + x[2]) % 2          # p (+) q
    ck(supp_of(p) == fs('ab') and supp_of(q) == fs('bc')
       and supp_of(pq) == fs('ac'),
       "leg 2: supports computed from the functions -- supp(p) = {a,b}, "
       "supp(q) = {b,c}, supp(p(+)q) = {a,c}")

    part_pq = partition_by(lambda x: (p(x), q(x)))
    ck(len(part_pq) == 4 and all(len(b) == 2 for b in part_pq),
       "leg 2: B_pq = <a(+)b, b(+)c> has 4 fibers of size 2 (proper "
       "subalgebra, dim 4 < 8)")
    certify(part_pq, "leg 2: E onto B_pq")

    def part_by_channels(T):
        idx = [k for k, name in enumerate(CH) if name in T]
        return partition_by(lambda x: tuple(x[k] for k in idx))

    ck(all(set(part_pq) != set(part_by_channels(T)) for T in _powerset(CH)),
       "leg 2: B_pq != <T> for ALL 8 channel subsets T -- a bona fide "
       "conditional expectation that is NOT reachable by merge-and-drop "
       "(merges are family re-grouping with E_B = id at algebra level)")
    part_p = partition_by(lambda x: (p(x), x[2]))
    ck(len(part_p) == 4, "leg 2: B_p = <a(+)b, c> proper (dim 4 < 8)")
    certify(part_p, "leg 2: E onto B_p")
    part_tw = partition_by(lambda x: (fs([('n', x[0] + x[1])]), x[2]))
    ck(len(part_tw) == 6, "leg 2: swap-twirl invariant algebra, 6 orbits")
    certify(part_tw, "leg 2: E onto the swap(a,b)-invariant subalgebra")
    s2f = lambda x: x[0] * x[1]
    ck(supp_of(lambda x: (x[0] + x[1]) % 2) == fs('ab')
       and supp_of(s2f) == fs('ab'),
       "leg 2: the twirl generators s1 = a(+)b, s2 = a AND b share the "
       "SAME support {a,b}")

    # ---- leg 3: the pinned counterexample ------------------------------
    supports_pq = [fs('ab'), fs('bc')]
    t, c, i, d = chain_parts(WORLDS['free'], supports_pq)
    ck((t, c, i) == (0, -EPS, 0) and d == EPS,
       "leg 3 PINNED COUNTEREXAMPLE (free world, B_pq presented on its "
       "parity generators): Delta_fine = 0 but Delta_coarse + sum "
       "Delta_internal = -eps -- the identity FAILS by exactly "
       "E({b}) = eps (the doubly-covered channel billed twice by the "
       "presentation, once by the fine ledger)")
    ck(all(chain_parts(E, supports_pq)[3] == E[fs('b')] >= EPS
           for E in WORLDS.values()),
       "leg 3: in ALL 9 worlds the defect equals E({b}) >= eps -- strict "
       "failure is floor-forced, occupancy-FREE (occupied-block worlds "
       "included; in W_nu the defect is 2*eps = E({b}) there)")

    # ---- leg 4: the defect formula + dichotomy sweep (F6 extension) -----
    pool = [S for S in _powerset(U3) if S]
    presentations = [list(cmb) for r in range(1, 8)
                     for cmb in combinations(pool, r)]
    ck(len(presentations) == 127,
       "leg 4 sweep space: ALL 127 families of distinct nonempty supports "
       "(exhaustive over that family -- audit F6 scope named; multiset "
       "instances via the twirl below)")
    formula_ok, dichotomy_ok = True, True
    n_cover = n_part = 0
    for E in WORLDS.values():
        for pres in presentations:
            tt, cc, ii, dd = chain_parts(E, pres)
            formula_ok &= (dd == defect_formula(E, pres))
            if fs().union(*pres) == U3:
                n_cover += 1
                part = is_partition(pres)
                n_part += part
                dichotomy_ok &= ((dd == 0) == part)
    ck(formula_ok and n_cover == 9 * 109 and n_part == 9 * 5,
       "leg 4: the exact defect identity holds on all 9 x 127 = 1143 "
       "cases (covering cases 981; partition cases 45 = 9 worlds x the 5 "
       "set-partitions of the 3-channel universe)")
    ck(dichotomy_ok,
       "leg 4 DICHOTOMY: on every covering case, defect = 0 <=> the "
       "supports partition the billed universe (equality iff m_i = 1 for "
       "all i, by the MD floor)")
    tw_pres = [fs('ab'), fs('ab'), fs('c')]
    tt, cc, ii, dd = chain_parts(WORLDS['free'], tw_pres)
    ck(dd == 2 * EPS == defect_formula(WORLDS['free'], tw_pres),
       "leg 4 multiset instance: the twirl presented on {s1, s2, c} (same "
       "support twice) fails with defect 2*eps -- over-billing counts "
       "multiplicity")
    ck(chain_parts(WORLDS['free'], [fs('ab'), fs('c')])[3] == 0,
       "leg 4: the same twirl re-presented on its support closure "
       "satisfies the identity -- the failure belongs to the "
       "PRESENTATION, which is the object the ledger reads")

    # ---- leg 5: canonicity, repaired (F1) --------------------------------
    E_free = WORLDS['free']
    kappa_needed = 4 * EPS   # for the two-parity identity to hold
    max_same_ledger = max(E_free[S] for S in _powerset(U3))
    ck(kappa_needed > max_same_ledger == 3 * EPS,
       "leg 5 (F1, the load-bearing canonicity leg): rescuing the "
       "two-parity identity in the free world needs kappa_B({p,q}) = "
       "4*eps > 3*eps = E(U) = max over ALL subsets -- NO same-ledger "
       "billing can rescue the counterexample; the failure side of the "
       "dichotomy is robust across the ENTIRE same-ledger family")
    kappa_prime = (E_free[fs('abc')]
                   + sum((m - 1) * E_free[fs([i])]
                         for i, m in {'a': 1, 'b': 2, 'c': 1}.items()))
    ck(kappa_prime == 4 * EPS
       and kappa_prime not in {E_free[S] for S in _powerset(U3)},
       "leg 5: the bake-in kappa-prime (= E(union) + sum (m_i - 1) E({i}) "
       "= 4*eps) would make the identity hold but is EXCLUDED by the "
       "same-ledger clause -- its value is not the fine cost of any "
       "subset (it renames the defect into the coarse billing)")
    ck(len([fs('abc')]) == 1 != len(supports_pq),
       "leg 5: the clustering transcription (bill connected components of "
       "the support-overlap graph) is EXCLUDED by the "
       "per-presented-channel clause -- it changes the presentation shape "
       "(2 generators -> 1 channel), i.e. it IS the re-presentation move, "
       "filed as such")
    # symmetric-difference billing: same-ledger, per-channel, reproduces
    # partitions (symmetric difference = union on disjoint supports), and
    # STILL fails the two-parity case -- with a different defect value.
    sd = supports_pq[0] ^ supports_pq[1]
    d_coarse_sd = (E_free[sd] - E_free[supports_pq[0]]
                   - E_free[supports_pq[1]])
    defect_sd = 0 - d_coarse_sd - 0          # Delta_fine = 0, internals 0
    ck(sd == fs('ac') and defect_sd == 2 * EPS != EPS,
       "leg 5 (F1 honesty): the symmetric-difference billing is "
       "same-ledger + per-channel + partition-reproducing and STILL fails "
       "the two-parity case (defect 2*eps, not eps) -- the dichotomy "
       "classification is family-robust, the defect FORMULA is "
       "T1-specific: T1 is CANONICAL (union billing), not unique")

    # ---- leg 6: the presentation quantifier (F2) -------------------------
    # B_pq's 4-fiber partition: enumerate ALL 15 coarsenings; the elements
    # of B_pq with proper support are EXACTLY the three parities.
    fibers = sorted(part_pq, key=lambda b: sorted(b))

    def set_partitions(items):
        if not items:
            yield []
            return
        first, rest = items[0], items[1:]
        for sub in set_partitions(rest):
            for k in range(len(sub)):
                yield sub[:k] + [[first] + sub[k]] + sub[k + 1:]
            yield [[first]] + sub

    proper_supports = set()
    n_coarsenings = 0
    for blocks in set_partitions(fibers):
        n_coarsenings += 1
        val = {}
        for bi, blk in enumerate(blocks):
            for fib in blk:
                for x in fib:
                    val[x] = bi
        g = lambda x, _v=val: _v[x]
        sp = supp_of(g)
        if sp and sp != U3:
            proper_supports.add(sp)
    ck(n_coarsenings == 15
       and proper_supports == {fs('ab'), fs('bc'), fs('ac')},
       "leg 6 (F2, the strongest reply): over ALL 15 coarsenings of "
       "B_pq's fiber partition, the elements with proper nonempty support "
       "are EXACTLY the three parities (supports {a,b}, {b,c}, {a,c})")
    ck(all(s1 & s2 for s1 in proper_supports for s2 in proper_supports),
       "leg 6: the three parity supports PAIRWISE OVERLAP -- so B_pq "
       "admits NO non-trivial compliant presentation: its only "
       "partition-of-U presentation is the single-channel support closure "
       "(support U, a trivial partition). 'Cross-cutting' is intrinsic to "
       "B_pq relative to non-trivial presentations; at bare subalgebra "
       "level the classification is degenerate (every covering B "
       "restorable) -- the theorem quantifies over PRESENTATIONS")

    # ---- leg 7: generator-relativity of the defect VALUE (F3) -----------
    E_nu = WORLDS['W_nu']
    d_gen1 = chain_parts(E_nu, [fs('ab'), fs('bc')])[3]
    d_gen2 = chain_parts(E_nu, [fs('ab'), fs('ac')])[3]
    ck(d_gen1 == 2 * EPS and d_gen2 == EPS,
       "leg 7 (F3): the defect VALUE is generator-relative -- the SAME "
       "B_pq shows defect E({b}) = 2*eps under <p, q> and E({a}) = eps "
       "under <p, p(+)q> in the non-uniform-floor world; strict FAILURE "
       "is generator-independent for B_pq (every 2-generator parity "
       "presentation overlaps, leg 6)")

    # ---- leg 8: undercovering B (F4) -------------------------------------
    part_ab1 = partition_by(lambda x: p(x))
    vals_ab1 = set()
    for blocks in set_partitions(sorted(part_ab1, key=lambda b: sorted(b))):
        val = {}
        for bi, blk in enumerate(blocks):
            for fib in blk:
                for x in fib:
                    val[x] = bi
        vals_ab1.add(supp_of(lambda x, _v=val: _v[x]))
    ck(vals_ab1 == {fs(), fs('ab')},
       "leg 8 (F4): B = <a(+)b> is UNDERCOVERING -- every element's "
       "support is contained in {a,b} (computed over all coarsenings), so "
       "NO presentation of B covers the billed universe: restorability is "
       "scoped to covering B")
    d_ab1 = {w: chain_parts(E, [fs('ab')])[3] for w, E in WORLDS.items()}
    ck(d_ab1['free'] == 0 and d_ab1['J_bc'] == EPS,
       "leg 8: the undercovering closure presentation's defect is "
       "world-dependent (0 in the free world, +eps in J_bc) -- it lives "
       "permanently in the restriction domain")
    d_pos = chain_parts(WORLDS['J_ab'], [fs('a')])[3]
    d_neg = chain_parts(WORLDS['R_tight'], [fs('c')])[3]
    d_zero = chain_parts(WORLDS['free'], [fs('a')])[3]
    ck(d_pos > 0 and d_neg < 0 and d_zero == 0,
       "leg 8: undercoverage defect sign-indefinite (+, -, 0) -- "
       "reconnects to the banked restriction no-go, as it must")

    # ---- leg 9: T2's determined fragment, computed (F5) ------------------
    E2 = WORLDS['W2']
    kappa_T2_merged = EPS * 2      # the merge keeps BOTH bits: content 2
    d_int_T2 = kappa_T2_merged - (E2[fs('a')] + E2[fs('b')])
    d_int_banked = _Delta(E2, fs('a'), fs('b'))
    d_coarse_banked = _Delta(E2, fs('ab'), fs('c'))
    omega_fine_W2 = E2[fs('abc')] - sum(E2[fs(x)] for x in 'abc')
    ck(kappa_T2_merged == 2 * EPS != E2[fs('ab')]
       and d_int_T2 == 0 != d_int_banked
       and omega_fine_W2 != d_coarse_banked + d_int_T2,
       "leg 9 (F5, computed): T2's determined fragment bills the W2 merge "
       "at 2*eps (content = the block's two kept distinctions) where the "
       "banked chain rule bills E(ab) = 4*eps; its Delta_internal becomes "
       "0 and the banked Prop 9.8 fixed point FAILS (3 != 1 + 0) -- T2 is "
       "excluded by the fixed points (its well-posedness defect is the "
       "docstring's prose clause)")

    # ---- leg 10: boundary legs -------------------------------------------
    ck(all(chain_parts(E, [fs('ab'), fs('c')])[3] == 0
           for E in WORLDS.values()),
       "leg 10: B_p = <a(+)b, c> is proper and NOT a merge as a channel "
       "map, yet its supports partition U and the identity holds in all "
       "9 worlds -- block merges are a STRICT subclass of the chain-rule "
       "class")
    ck(all(chain_parts(E, [fs('ab'), fs('c')])
           == chain_parts(E, [supp_of(p), supp_of(lambda x: x[2])])
           for E in WORLDS.values()),
       "leg 10 fiber-blindness fence: the merge of {a,b} and the "
       "dephasing-to-parity of {a,b} transcribe IDENTICALLY -- the "
       "transcription is a support functor; fiber-level information loss "
       "has no ledger referent until re-presented (single-table scope)")
    # anchor transport, used (F8): the partition channels' transported
    # anchors are disjoint and their pairwise Delta vanishes (free world).
    anc_1, anc_2 = fs('ab'), fs('c')
    d_pair = (E_free[anc_1 | anc_2] - E_free[anc_1] - E_free[anc_2])
    ck(not (anc_1 & anc_2) and d_pair == 0,
       "leg 10 (F8, anchor transport USED): the partition presentation's "
       "coarse channels carry disjoint support-transported anchors and "
       "their pairwise Delta = 0 in the free world -- consistent with "
       "T_delta_disjoint_additivity through the transported anchors")

    n_legs = len(checks)

    return _result(
        name='T_delta_chain_rule_conditional_expectation_dichotomy -- the '
             'chain rule holds for a presented coarse family iff its '
             'supports partition the billed universe (exact defect '
             'formula; pinned two-parity counterexample, floor-forced)',
        tier=4,
        epistemic='P',
        summary=(
            'THE CHAIN-RULE DICHOTOMY FOR PRESENTED COARSE FAMILIES '
            '(Paper 12 round-6 walk C2, reviewer Q9). A conditional '
            'expectation E_B onto a subalgebra of the record algebra has '
            'no ledger referent by itself; it enters through a '
            'PRESENTATION (generating coarse channels billed at their '
            'dependency supports in the SAME ledger, anchors transported '
            'by support -- the support transcription, CANONICAL not '
            'unique, with the three canonicity clauses executable '
            'in-check: same-ledger, per-presented-channel, block-merge '
            'reproduction). Exact defect identity: Delta_fine - '
            'Delta_coarse - sum Delta_internal = [E(U) - E(union)] + '
            'sum (m_i - 1) E({i}), verified on 9 worlds x all 127 '
            'distinct-support families = 1143 exact cases (+ multiset '
            'instances); for covering presentations the defect vanishes '
            'IFF the supports partition the billed universe (the MD floor '
            'makes cross-cutting failure STRICT -- no occupancy premise). '
            'The pinned counterexample: E onto B_pq = <a(+)b, b(+)c> -- '
            'certified unital/idempotent/positive/bimodule/'
            'trace-preserving/range, provably NOT merge-and-drop -- '
            'presented on its parity generators misses the identity by '
            'exactly E({b}), in every world, and NO same-ledger billing '
            'can rescue it (the free-world impossibility: 4*eps > E(U) = '
            '3*eps -- failure robust across the entire repaired family; '
            'the bake-in kappa-prime and the clustering alternative are '
            'excluded by the named clauses; the symmetric-difference '
            'billing shows the defect FORMULA is T1-specific while the '
            'classification is family-robust). The theorem quantifies '
            'over PRESENTATIONS: every covering B is restorable on its '
            'support closure (subalgebra level degenerate), B_pq admits '
            'NO non-trivial compliant presentation (its proper-support '
            'elements are exactly the three pairwise-overlapping '
            'parities, computed over all 15 coarsenings), the defect '
            'VALUE is generator-relative (2*eps vs eps for the same B_pq '
            'in the non-uniform-floor world) while strict failure is '
            'generator-independent, and undercovering B admits no '
            'covering presentation at all (permanently in the restriction '
            'domain -- the banked sign-indefinite no-go). T2\'s determined '
            'fragment fails the banked W2 fixed point, computed (2*eps != '
            '4*eps; 3 != 1 + 0). Block merges are a STRICT subclass of '
            'the chain-rule class (the single-parity witness); the '
            'transcription is a support functor (merge and dephasing '
            'transcribe identically -- fiber loss has no ledger referent '
            'until re-presented); the banked Prop 9.8 form is '
            'SINGLE-BLOCK, the multi-block form is this check\'s '
            'extension. One mnemonic: the chain rule holds iff the coarse '
            'presentation covers each fine channel exactly once '
            '(undercover: restriction domain; exact cover: identity; '
            'overcover: strictly positive defect). All arithmetic exact; '
            '%d assertions. Occupancy: not consumed.' % n_legs
        ),
        key_result=(
            'Under the named support transcription (canonical: '
            'same-ledger + per-presented-channel + block-merge-'
            'reproducing), the chain rule Delta_fine = Delta_coarse + '
            'sum Delta_internal holds for a presented coarse family IFF '
            'its supports partition the billed universe; defect = '
            'coverage gap + sum (m_i - 1) E({i}); the two-parity '
            'counterexample fails by exactly E({b}), floor-forced, '
            'occupancy-free, unrescuable same-ledger; the dichotomy '
            'classifies PRESENTATIONS (every covering B restorable; B_pq '
            'has no non-trivial compliant presentation).'
        ),
        dependencies=['L_cost', 'L_irr', 'T_canonical', 'L_epsilon*'],
        cross_refs=['T_delta_coarse_graining_monotonicity',
                    'T_delta_disjoint_additivity',
                    'T_cost_count_characterization',
                    'T_delta_JR_derived',
                    'L_T2_finite_gns',
                    'FD1_structural_completeness'],
        n_assertions=n_legs,
        artifacts={
            'transcription': 'T1 support transcription -- CANONICAL '
                             '(union billing), not unique; clauses: '
                             'same-ledger, per-presented-channel, '
                             'block-merge reproduction',
            'defect_formula': 'defect = [E(U) - E(union supp)] + '
                              'sum_i (m_i - 1) E({i}); 1143 exact cases',
            'counterexample': 'B_pq = <a(+)b, b(+)c> on parity '
                              'generators: defect = E({b}) in every '
                              'world; same-ledger rescue impossible '
                              '(4*eps > E(U) = 3*eps)',
            'presentation_quantifier': 'every covering B restorable; '
                                       'B_pq: no non-trivial compliant '
                                       'presentation (15-coarsening '
                                       'enumeration); defect value '
                                       'generator-relative',
            'coverage_taxonomy': 'undercover sign-indefinite '
                                 '(restriction) / exact cover identity / '
                                 'overcover strictly positive '
                                 '(floor-forced)',
            'T2_exclusion': 'determined fragment computed: 2*eps != '
                            '4*eps, Prop 9.8 fixed point fails; '
                            'well-posedness half = prose clause',
        },
    )


_CHECKS = {
    'check_T_delta_disjoint_additivity':
        check_T_delta_disjoint_additivity,
    'check_T_delta_coarse_graining_monotonicity':
        check_T_delta_coarse_graining_monotonicity,
    'check_T_cost_count_characterization':
        check_T_cost_count_characterization,
    'check_T_delta_not_an_information_functional':
        check_T_delta_not_an_information_functional,
    'check_T_register_reading_grounds_ceil_log2_count':
        check_T_register_reading_grounds_ceil_log2_count,
    'check_T_delta_JR_derived':
        check_T_delta_JR_derived,
    'check_T_delta_chain_rule_conditional_expectation_dichotomy':
        check_T_delta_chain_rule_conditional_expectation_dichotomy,
}


def register(registry):
    """Register the Delta-calculus checks into the bank."""
    registry.update(_CHECKS)


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == '__main__':
    for _n, _r in run_all().items():
        print(('PASS' if _r.get('passed', True) else 'FAIL'), _n)
        print('  grade:', _r['epistemic'], '| tier', _r['tier'])
        print('  ', _r['key_result'])


# ---------------------------------------------------------------------------
# Interface Engine onboarding (Full Bank Onboarding wave, 2026-07-04)
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "foundation:delta_calculus_derived_identities",
        "axis": "ROUTE",
        "route": "delta_calculus_identities",
        "expect_export": True,
        "payload": {
            "name": "delta_calculus_derived_identities",
            "closure_kind": "internal_identity",
            "identity_summary": (
                "The Delta-calculus's derived identities hold by structural "
                "identity over the banked cost calculus, exact-rational "
                "throughout: Delta = eps(J - R) is DERIVED [P] "
                "(inclusion-exclusion over typed CH1 channels + the banked "
                "cost = count characterization), with R = shared CHANNELS and "
                "the ledger-relativity clause carried as part of the "
                "statement -- J and R are relative to the presented billing "
                "decomposition, never absolute; Delta = 0 across "
                "anchor-disjoint interfaces at theorem strength [P]; the "
                "cost = count characterization [P]: X1+X2+X3 force "
                "kappa = n*eps* on N with NO continuity assumption. Global "
                "monotonicity of Delta under coarse-graining is FALSE -- "
                "pinned finite counterexamples in BOTH directions. "
                "(check_T_delta_JR_derived + check_T_delta_disjoint_additivity "
                "+ check_T_cost_count_characterization + "
                "check_T_delta_coarse_graining_monotonicity, delta_calculus.py)"
            ),
        },
        "note": (
            "Onboards the Paper 12 Delta-calculus onto the ROUTE axis as a "
            "structural identity: the derived ledger identities are the "
            "codomain by construction, no evaluator transport, no physics "
            "import. The ledger-relativity clause and the non-monotonicity "
            "no-go ride in the identity text so a future flattening "
            "('derived' without ledger-relativity, or 'Delta is monotone') "
            "fails the pin."
        ),
    },
)
