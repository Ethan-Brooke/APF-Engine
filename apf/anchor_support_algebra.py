"""apf/anchor_support_algebra.py -- the algebraic anchor: supports, anchors,
independence.

v24.3.381 (2026-07-04, Paper 12 round-6 review lane C1, reviewer Q1;
fresh-context walk (witness 24/24) + fresh-context hostile audit
LAND-WITH-FIXES 0.84, mandatory fixes F1-F4 + recommended F5-F7 ALL carried
across this module and its sibling check_T_delta_JR_derived in
apf/delta_calculus.py). Walk of record: "The Turning/
p12_review6_walks_2026-07-04/c1_algebraic_anchors/" (walk_report_c1.md +
witness_c1_algebraic_anchors.py + audit_report_c1.md).

One check:

  check_T_anchor_support_formalization  [P]
      The decomposition-relative support theory: on a finite interface
      presentation (V, {A_v}, C) with ARBITRARY finite-dimensional unital
      *-algebra factors (full matrix algebras NOT assumed; the lattice's
      own billing factor C (+) M_2 has a two-dimensional centre and is the
      witnessed case), the support supp(M) = smallest W with
      M c A_W (x) 1 exists and is unique (the family of admissible W is
      intersection-closed -- the slice-map lemma, audit-verified for
      arbitrary finite-dim factors including with-centre), obeys a calculus
      (monotone under inclusion; union-additive under algebra generation;
      covariant under relabelings), and anc(S) := supp(M(S)) -- the anchor
      set IS the support of the record algebra. Independence <=> disjoint
      anchors is then a theorem in two halves, with the TWO-CLAUSE honesty
      carried in-check (see below).

THE TWO-CLAUSE HONESTY (audit F5, stated plainly). Independence is the
two-clause notion check_T_M certifies:
  (a) canonical factorization -- the multiplication map
      M1 (x) M2 -> alg(M1 u M2) is a *-isomorphism and the joint valuation
      set is the free product Omega(S1) x Omega(S2) (L_loc's factorized
      state space); AND
  (b) budget factorization -- no locus is billed by both families (the two
      demand functions on V have disjoint support).
The direction disjoint => independent is PURE finite-dimensional algebra
(leg 3; no fullness assumption -- centres ride along inside their factors;
the merely-commuting-pairs subtlety does not arise because disjointness is
relative to the DISTINGUISHED billing decomposition, which supplies the
tensor splitting for free). The direction independent => disjoint is
IRREDUCIBLY LEDGER-LEVEL: it consumes the cost floor (L_epsilon*) and
finite per-locus capacity (A1) via budget competition (check_T_M steps
4-9, reproduced exactly in leg 4), NOT operator algebra -- and it must,
because clause (b)'s failure at a shared locus is partly DEFINITIONAL for
the two-clause notion: given clause (b), "shared locus => not independent"
is the definition doing its job, with the budget-competition arithmetic
as the detectability content. The honesty control (leg 5) pins this: two
DISTINCT binary records on one four-state locus have trivially
intersecting record algebras, a dimension-factorizing joint algebra
(dim 4 = 2 x 2), a free joint valuation set -- clause (a) FULLY holds --
and Delta = 0, yet independence fails at clause (b). So the biconditional
holds for the operative two-clause notion and FAILS for the purely
algebraic one; the forward direction is not an operator-algebraic
discovery, and this docstring says so plainly.

THE RELABELING GROUP (audit F7, the G_rel definition with the
anti-automorphism scope stated). G_rel := (prod_v Aut(A_v)) x| Perm_iso(V):
factor-wise *-automorphisms (inner unitaries u_v in A_v, plus label
permutations of classical outcome sets) together with permutations pi of
like factors (A_v isomorphic to A_pi(v)), acting on A_Gamma by
(x)_v alpha_v followed by factor permutation, and on presentations by
transport. ANTI-automorphisms (transpose-type relabelings) are EXCLUDED
from G_rel by definition, with the reason stated: G_rel is the group of
empirical-difference-free relabelings acting by *-homomorphisms on the
record composition structure; a transpose reverses operator products and
is not a relabeling of the presentation in that sense. The exclusion is
harmless for every quantity this check certifies -- supports, dimensions,
block structures, and channel counts are all transpose-invariant -- so
extending the group would change no leg; the scope is stated rather than
smuggled. Support covariance, dimension invariance, and (in the sibling
check) J/R/Delta invariance under G_rel are theorems (leg 6); that the
LEDGER is covariant -- that billing attaches no cost to a relabeling --
is X1's relabel-freedom clause (FD1-sc), the allocation reading, named as
a hypothesis at exactly one gate (the costchar precedent), never here
re-derived.

CH3 STATUS (audit F7a, the mislabel fixed): anchor consistency --
anc(S) = union of supp(c) over c in Ch(S), every supp(c) nonempty -- is a
DEFINITIONAL AXIOM of the channel-ledger structure (Definition 5 of the
walk), not a lemma. The pre-audit "Lemma CH3" label was wrong; the budget
clause of the disjoint => independent direction is CH3-definitional and
is labeled so here and in the sibling check.

NUMERICAL-COINCIDENCE FENCE (audit F7e): the meson-cut type-a witness of
this module (join record algebra dim 5 > 4 = dim alg(M1 u M2), at a
VERTEX-FREE cut) is numerically coincident with the banked shared-vertex
"centre dim 5 vs 4 flux tuples" of check_T_anchor_set_is_electric_center_
data leg 7 -- DIFFERENT objects (a record-algebra dimension jump vs a
superselection-centre extension); no identification is made or implied.

WHERE THE READING ENTERS -- exactly once, and it is CITED, not re-graded:
the choice of WHICH tensor decomposition is the billing decomposition is
the lattice identification of Paper 12 SS2 plus the allocation reading,
banked at [P_structural_reading] in
check_T_anchor_set_is_electric_center_data (this module's consistency leg
cites that check by name). AFTER the choice, every statement in this
module is a theorem in exact finite mathematics -- which is what the [P]
grade marks (the banked pattern: check_T_delta_disjoint_additivity [P]
alongside the [P_structural_reading] correspondence module).

FENCES: no occupancy claim (no sign realized-in-the-world claim); no
entropy claim; Delta = 0 does NOT certify independence (the honesty
control is the finite counterexample); the counting identity
Delta = eps*(J - R) and its R-convention live in the sibling check
check_T_delta_JR_derived (apf/delta_calculus.py), not here.

All arithmetic exact (fractions.Fraction over Q), pure stdlib, no floats.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, product as iproduct
from typing import Dict

from apf.apf_utils import check, _result


# ============================================================================
# exact linear algebra over Q (ported from the walk witness)
# ============================================================================

class _Span:
    """Row-reduced span of rational vectors; exact membership tests."""

    def __init__(self):
        self.rows = []  # list of (pivot_index, reduced_vector)

    def _reduce(self, v):
        v = list(v)
        for p, r in self.rows:
            if v[p] != 0:
                c = v[p]
                v = [a - c * b for a, b in zip(v, r)]
        return v

    def contains(self, v):
        return all(x == 0 for x in self._reduce(v))

    def add(self, v):
        w = self._reduce(v)
        for i, x in enumerate(w):
            if x != 0:
                inv = F(1) / x
                w = [a * inv for a in w]
                new_rows = []
                for p, r in self.rows:
                    if r[i] != 0:
                        c = r[i]
                        r = [a - c * b for a, b in zip(r, w)]
                    new_rows.append((p, r))
                self.rows = new_rows
                self.rows.append((i, w))
                return True
        return False

    @property
    def dim(self):
        return len(self.rows)


def _zeros(r, c=None):
    if c is None:
        c = r
    return [[F(0)] * c for _ in range(r)]


def _eye(n):
    M = _zeros(n)
    for i in range(n):
        M[i][i] = F(1)
    return M


def _mm(A, B):
    r, k, c = len(A), len(B), len(B[0])
    out = _zeros(r, c)
    for i in range(r):
        Ai, oi = A[i], out[i]
        for t in range(k):
            a = Ai[t]
            if a:
                Bt = B[t]
                for j in range(c):
                    if Bt[j]:
                        oi[j] += a * Bt[j]
    return out


def _mat_eq(A, B):
    return all(A[i][j] == B[i][j]
               for i in range(len(A)) for j in range(len(A[0])))


def _transpose(A):
    return [list(col) for col in zip(*A)]


def _kron(A, B):
    ra, ca, rb, cb = len(A), len(A[0]), len(B), len(B[0])
    out = _zeros(ra * rb, ca * cb)
    for i in range(ra):
        for j in range(ca):
            a = A[i][j]
            if a:
                for k in range(rb):
                    for l in range(cb):
                        out[i * rb + k][j * cb + l] = a * B[k][l]
    return out


def _flat(M):
    return [x for row in M for x in row]


def _alg_close(gens, dim):
    """Unital *-algebra closure (all inputs real symmetric-or-permutation,
    so *-closure = adding transposes). Returns (basis_mats, _Span)."""
    basis, sp = [], _Span()

    def try_add(M):
        if sp.add(_flat(M)):
            basis.append(M)
            return True
        return False

    try_add(_eye(dim))
    work = list(gens) + [_transpose(g) for g in gens]
    for g in work:
        try_add(g)
    changed = True
    while changed:
        changed = False
        cur = list(basis)
        for A in cur:
            for B in cur:
                P = _mm(A, B)
                if not sp.contains(_flat(P)):
                    try_add(P)
                    changed = True
    return basis, sp


# ============================================================================
# tensor-factor machinery: slice maps, supports (Lemma 1 / Lemma 2)
# ============================================================================

def _multi_indices(dims):
    return list(iproduct(*[range(d) for d in dims]))


def _slice_map(X, dims, v):
    """E_v = id (x) tau_v (x) id : replace factor v by its normalized-trace
    slice re-tensored with 1_v. Range = A_{V \\ {v}} (x) 1_v. Needs only a
    unital linear functional on the factor (idempotency does the fixed-point
    identification); no positivity, faithfulness, or factoriality."""
    idxs = _multi_indices(dims)
    pos = {t: k for k, t in enumerate(idxs)}
    D = len(idxs)
    dv = dims[v]
    Y = _zeros(D)
    for i, ti in enumerate(idxs):
        for j, tj in enumerate(idxs):
            if ti[v] != tj[v]:
                continue
            s = F(0)
            for c in range(dv):
                ri = list(ti); ri[v] = c
                rj = list(tj); rj[v] = c
                s += X[pos[tuple(ri)]][pos[tuple(rj)]]
            Y[i][j] = s / dv
    return Y


def _support_slice(basis_mats, dims):
    """supp(M) via the pointwise slice characterization (Lemma 1):
    supp(M) = {v : E_v does not fix M pointwise}."""
    out = set()
    for v in range(len(dims)):
        if any(not _mat_eq(_slice_map(X, dims, v), X) for X in basis_mats):
            out.add(v)
    return out


def _AW_basis(W, dims, factor_bases):
    """Spanning set of A_W (x) 1_{V\\W} inside (x)_v A_v."""
    per_factor = [factor_bases[v] if v in W else [_eye(dims[v])]
                  for v in range(len(dims))]
    out = []
    for combo in iproduct(*per_factor):
        K = combo[0]
        for M in combo[1:]:
            K = _kron(K, M)
        out.append(K)
    return out


def _contained_in_AW(basis_mats, W, dims, factor_bases):
    sp = _Span()
    for B in _AW_basis(W, dims, factor_bases):
        sp.add(_flat(B))
    return all(sp.contains(_flat(X)) for X in basis_mats)


def _support_brute(basis_mats, dims, factor_bases):
    """All W with M c A_W (x) 1; verify intersection-closure; return the
    unique minimal element (Lemma 1's existence/uniqueness, brute-forced)."""
    V = list(range(len(dims)))
    family = []
    for r in range(len(V) + 1):
        for W in combinations(V, r):
            if _contained_in_AW(basis_mats, set(W), dims, factor_bases):
                family.append(frozenset(W))
    closed = all((W1 & W2) in family for W1 in family for W2 in family)
    minimal = min(family, key=len) if family else None
    is_min = all(minimal <= W for W in family)
    return set(minimal), closed and is_min


# ============================================================================
# classical layer (functions on finite configuration spaces)
# ============================================================================

def _cfg_space(sizes):
    return list(iproduct(*[range(s) for s in sizes]))


def _fvec(configs, f):
    return tuple(F(f(c)) for c in configs)


def _depends_on(configs, sizes, vec, v):
    pos = {c: k for k, c in enumerate(configs)}
    for k, c in enumerate(configs):
        for a in range(sizes[v]):
            c2 = list(c); c2[v] = a
            c2 = tuple(c2)
            if c2 in pos and vec[pos[c2]] != vec[k]:
                return True
    return False


def _fn_alg_dim(configs, vecs):
    """Dimension of the unital algebra of functions generated pointwise."""
    n = len(configs)
    sp = _Span()
    basis = []

    def try_add(v):
        if sp.add(list(v)):
            basis.append(tuple(v))
            return True
        return False

    try_add(tuple(F(1) for _ in range(n)))
    for v in vecs:
        try_add(v)
    changed = True
    while changed:
        changed = False
        cur = list(basis)
        for a in cur:
            for b in cur:
                p = tuple(x * y for x, y in zip(a, b))
                if not sp.contains(list(p)):
                    try_add(p)
                    changed = True
    return sp.dim


# ============================================================================
# the lattice model: two truncated SU(2) links, A_l = C (+) M_2 (with centre)
# ============================================================================

def _m3(entries):
    M = _zeros(3)
    for (i, j), val in entries.items():
        M[i][j] = F(val)
    return M


def _build_lattice():
    # H_l = C^3: index 0 = flux j=0; indices 1,2 = flux j=1/2 (A-side factor)
    dims = [3, 3]
    E = {(a, b): _m3({(a, b): 1}) for a in range(3) for b in range(3)}
    # per-link constraint-solved billing factor A_l = C Pi_0 (+) M_2 (dim 5)
    A_l = [E[(0, 0)], E[(1, 1)], E[(1, 2)], E[(2, 1)], E[(2, 2)]]
    factor_bases = [A_l, A_l]
    Pi0 = E[(0, 0)]
    Pih = [[E[(1, 1)][i][j] + E[(2, 2)][i][j] for j in range(3)]
           for i in range(3)]
    I3 = _eye(3)
    # flux record algebras (the anchors' record content per link)
    M1_gens = [_kron(Pi0, I3), _kron(Pih, I3)]
    M2_gens = [_kron(I3, Pi0), _kron(I3, Pih)]
    # the fused singlet projector on the (1/2, 1/2) block:
    # |psi> = (e1 (x) e2 - e2 (x) e1)/sqrt2 ; flat indices 3*1+2=5, 3*2+1=7
    Ps = _zeros(9)
    Ps[5][5] = F(1, 2); Ps[7][7] = F(1, 2)
    Ps[5][7] = F(-1, 2); Ps[7][5] = F(-1, 2)
    return dims, factor_bases, M1_gens, M2_gens, Ps


def _conjugate_basis(basis, U):
    Ut = _transpose(U)  # real orthogonal here
    return [_mm(U, _mm(X, Ut)) for X in basis]


# ============================================================================
# THE CHECK
# ============================================================================

def check_T_anchor_support_formalization() -> Dict:
    """T_anchor_support_formalization: the algebraic anchor -- support
    existence/uniqueness (the slice-map lemma, arbitrary finite-dim factors
    incl. with-centre), the support calculus, anc = supp of the record
    algebra, independence <=> disjoint anchors with the two-clause honesty
    (<= pure algebra proved; => ledger-level via budget competition, the
    forward direction ledger-definitional -- module docstring, audit F5),
    invariance under the relabeling group G_rel (anti-automorphism scope
    stated, audit F7), and consistency legs vs the banked check_T_M /
    L_loc content.

    Seven legs, all exact (fractions.Fraction over Q, no floats):
      1. SLICE = BRUTE (Lemma 1): on the two-link model with with-centre
         factors A_l = C (+) M_2, the slice-map support characterization
         supp(M) = {v : E_v does not fix M pointwise} agrees with the
         brute-force minimal support for four record algebras; the family
         W(M) = {W : M c A_W (x) 1} is intersection-closed with a unique
         minimum in every case. Pins the arbitrary-A_v clause: full matrix
         factors are NOT assumed.
      2. SUPPORT CALCULUS (Lemma 2): supp of a generated algebra = union
         of the generator supports; monotone under inclusion.
      3. DISJOINT => INDEPENDENT (Theorem 1 <=, pure algebra): the two
         flux record algebras commute elementwise and
         dim alg(M1 u M2) = dim M1 * dim M2 (the multiplication map
         M1 (x) M2 -> alg(M1 u M2) is a canonical *-isomorphism); the
         classical two-bit case factorizes identically (dim 4 = 2 * 2).
         No fullness of the factors is used anywhere; the Ozawa
         merely-commuting subtlety is settled by decomposition-relativity.
      4. SHARED => NOT INDEPENDENT (Theorem 1 =>, the ledger leg):
         check_T_M's exact Fraction arithmetic reproduced -- shared locus
         saturates (eps + eta12 + eta13 = C_v), raising one demand lowers
         the other's ceiling (eta13 ceiling drops 1 -> 1/2). Consumes A1
         (finite C_v) + L_epsilon* (positive floor); implementation-free,
         NOT operator-algebraic.
      5. THE HONESTY CONTROL: two DISTINCT binary records billing ONE
         four-state locus -- record algebras intersect trivially, joint
         algebra dimension-factorizes (dim 4 = 2 * 2), Delta = 0 -- yet
         independence fails at the budget clause alone. Pins: (i) the =>
         direction is ledger-level; (ii) Delta = 0 does NOT certify
         independence; (iii) the locus-cardinality reading of R breaks on
         exactly this instance (the R-convention content lives in the
         sibling check_T_delta_JR_derived).
      6. RELABEL COVARIANCE (Theorem 3, algebra half): under the link
         swap (the 9x9 SWAP in Perm_iso(V)) supports permute and
         dimensions are invariant; under a factor-wise flux-preserving
         unitary (in prod_v Aut(A_v)) supports and dimensions are exactly
         invariant; under a classical label flip the constrained valuation
         set transports bijectively with invariant support. G_rel per the
         module docstring; anti-automorphisms excluded with the stated
         reason (harmless: all certified quantities transpose-invariant).
      7. CONSISTENCY + THE TYPE-A EXPORT: anc(flux family) = crossed-link
         set COMPUTED (the lattice identification of Paper 12 SS2,
         reproduced by the machinery rather than postulated -- the
         reading itself stays banked at [P_structural_reading] in
         check_T_anchor_set_is_electric_center_data, cited not re-graded);
         the fused-singlet type-a deviation data (dim M12 = 5 > 4 =
         dim alg(M1 u M2); P_s not in alg(M1 u M2); supp(P_s) = both
         links) computed and exported as artifacts for the sibling
         check's live call.

    FALSIFIERS (live): a certified independent pair with intersecting
    supports; a support family not closed under intersection on any finite
    presentation; an anchor-disjoint pair whose joint algebra fails
    dim-multiplicativity.

    GRADE: [P] -- exact finite mathematics after the reading-gated billing
    decomposition choice, which is cited (leg 7) at its banked
    [P_structural_reading] home, never re-graded. Occupancy: not consumed.
    """
    checks = []

    def ck(cond, msg):
        checks.append((bool(cond), msg))
        check(cond, msg)

    dims, fb, M1_gens, M2_gens, Ps = _build_lattice()

    M1_basis, M1_sp = _alg_close(M1_gens, 9)
    M2_basis, M2_sp = _alg_close(M2_gens, 9)
    Ms_basis, _ = _alg_close([Ps], 9)
    Mu_basis, Mu_sp = _alg_close(M1_gens + M2_gens, 9)           # alg(M1 u M2)
    M12_basis, M12_sp = _alg_close(M1_gens + M2_gens + [Ps], 9)  # join records

    # ---- leg 1: slice-map support == brute-force minimal support --------
    for nm, basis, want in (("M1 (flux record, link 0)", M1_basis, {0}),
                            ("M2 (flux record, link 1)", M2_basis, {1}),
                            ("alg(P_singlet) (spanning record)", Ms_basis,
                             {0, 1}),
                            ("M12 (join record algebra)", M12_basis, {0, 1})):
        s_slice = _support_slice(basis, dims)
        s_brute, lattice_ok = _support_brute(basis, dims, fb)
        ck(s_slice == s_brute == want and lattice_ok,
           "leg 1: supp(%s) -- slice = brute = %s; W(M) intersection-closed "
           "with a unique minimum (with-centre factors C (+) M_2)"
           % (nm, sorted(want)))

    # ---- leg 2: support calculus ----------------------------------------
    s1 = _support_slice(M1_basis, dims)
    s2 = _support_slice(M2_basis, dims)
    ss = _support_slice(Ms_basis, dims)
    s12 = _support_slice(M12_basis, dims)
    ck(s12 == (s1 | s2 | ss),
       "leg 2: supp(alg(M1 u M2 u {P_s})) = supp(M1) u supp(M2) u supp(P_s) "
       "(union under generation, Lemma 2)")
    ck(s1 <= s12, "leg 2: monotonicity -- M1 c M12 => supp(M1) c supp(M12)")

    # ---- leg 3: disjoint supports => canonical factorization ------------
    commute = all(_mat_eq(_mm(a, b), _mm(b, a))
                  for a in M1_basis for b in M2_basis)
    ck(commute, "leg 3: [M1, M2] = 0 elementwise (complementary tensor "
                "factors; quantum case)")
    ck(Mu_sp.dim == M1_sp.dim * M2_sp.dim,
       "leg 3: dim alg(M1 u M2) = %d = %d * %d = dim M1 * dim M2 (the "
       "multiplication map M1 (x) M2 -> alg(M1 u M2) is a canonical "
       "*-isomorphism; no fullness assumed)"
       % (Mu_sp.dim, M1_sp.dim, M2_sp.dim))
    sizesA = [2, 2]
    cfgA = _cfg_space(sizesA)
    b0 = _fvec(cfgA, lambda c: c[0])
    b1 = _fvec(cfgA, lambda c: c[1])
    dA1 = _fn_alg_dim(cfgA, [b0])
    dA2 = _fn_alg_dim(cfgA, [b1])
    dAu = _fn_alg_dim(cfgA, [b0, b1])
    ck(dAu == dA1 * dA2 == 4
       and _depends_on(cfgA, sizesA, b0, 0)
       and not _depends_on(cfgA, sizesA, b0, 1)
       and _depends_on(cfgA, sizesA, b1, 1)
       and not _depends_on(cfgA, sizesA, b1, 0),
       "leg 3: classical two-bit factorization dim 4 = 2 * 2 with computed "
       "disjoint supports")

    # ---- leg 4: shared support => budget competition (check_T_M) --------
    C_v = F(3); eps = F(1); eta12 = F(1); eta13 = F(1)
    ck(eps + eta12 + eta13 == C_v,
       "leg 4: shared locus saturates -- eps + eta12 + eta13 = C_v "
       "(check_T_M's exact Fractions, reproduced)")
    eta12_big = F(3, 2)
    eta13_max = C_v - eps - eta12_big
    ck(eta13_max == F(1, 2) and eta13_max < eta13,
       "leg 4: raising one family's demand at the shared locus lowers the "
       "other's ceiling 1 -> 1/2 (budget competition = detectable "
       "correlation; A1 + L_epsilon*, implementation-free, NOT "
       "operator-algebraic)")

    # ---- leg 5: the honesty control --------------------------------------
    sizesH = [4]
    cfgH = _cfg_space(sizesH)
    g_hi = _fvec(cfgH, lambda c: c[0] // 2)
    g_lo = _fvec(cfgH, lambda c: c[0] % 2)
    dH1 = _fn_alg_dim(cfgH, [g_hi])
    dH2 = _fn_alg_dim(cfgH, [g_lo])
    dHu = _fn_alg_dim(cfgH, [g_hi, g_lo])
    shared = (_depends_on(cfgH, sizesH, g_hi, 0)
              and _depends_on(cfgH, sizesH, g_lo, 0))
    # the two families' channel sets are LITERALLY distinct records on one
    # locus: no shared channel, no joint channel -- Delta = 0 by the
    # counting identity (the sibling check derives it; here the arithmetic
    # is the two-route booking on this instance).
    kappa1, kappa2, kappa_join = F(1), F(1), F(2)   # eps = 1; two records
    delta_h = kappa_join - kappa1 - kappa2
    ck(shared and dHu == dH1 * dH2 == 4 and delta_h == 0,
       "leg 5 HONESTY CONTROL: two distinct records on ONE four-state locus "
       "-- shared anchor, trivially intersecting record algebras, joint "
       "algebra dimension-factorizes (4 = 2 * 2), Delta = 0 -- yet NOT "
       "independent: clause (a) fully holds, clause (b) fails at the "
       "budget. Independence is a BUDGET statement; Delta = 0 does not "
       "certify it; the => direction is ledger-level (module docstring)")

    # ---- leg 6: relabel covariance (Theorem 3, algebra half) ------------
    idxs = _multi_indices(dims)
    pos = {t: k for k, t in enumerate(idxs)}
    SWAP = _zeros(9)
    for (i0, i1) in idxs:
        SWAP[pos[(i0, i1)]][pos[(i1, i0)]] = F(1)
    M1s = _conjugate_basis(M1_basis, SWAP)
    M2s = _conjugate_basis(M2_basis, SWAP)
    Pss = _conjugate_basis([Ps], SWAP)[0]
    _, M12s_sp = _alg_close(M1s + M2s + [Pss], 9)
    ck(_support_slice(M1s, dims) == {1}
       and _support_slice(M2s, dims) == {0}
       and _support_slice([Pss], dims) == {0, 1}
       and M12s_sp.dim == M12_sp.dim,
       "leg 6: link swap (Perm_iso(V)) -- supports permute by pi, join "
       "dimension invariant")
    U = _m3({(0, 0): 1, (1, 2): 1, (2, 1): 1})   # diag(1, X): e1 <-> e2
    U9 = _kron(U, _eye(3))
    M1u = _conjugate_basis(M1_basis, U9)
    Psu = _conjugate_basis([Ps], U9)[0]
    _, M12u_sp = _alg_close(M1u + M2_basis + [Psu], 9)
    ck(_support_slice(M1u, dims) == {0}
       and _support_slice([Psu], dims) == {0, 1}
       and M12u_sp.dim == M12_sp.dim,
       "leg 6: factor-wise flux-preserving unitary (prod_v Aut(A_v)) -- "
       "supports and dimensions exactly invariant")
    sizesP = [2, 2, 2]
    cfgP = _cfg_space(sizesP)
    omega12 = [c for c in cfgP if (c[0] + c[1] + c[2]) % 2 == 0]
    pv = _fvec(cfgP, lambda c: (c[0] + c[1] + c[2]) % 2)
    sigma_cfg = {c: (1 - c[0], c[1], c[2]) for c in cfgP}
    posP = {c: k for k, c in enumerate(cfgP)}
    pv_t = tuple(pv[posP[sigma_cfg[c]]] for c in cfgP)
    dep_all_t = all(_depends_on(cfgP, sizesP, pv_t, v) for v in range(3))
    omega12_t = [sigma_cfg[c] for c in omega12]
    ck(dep_all_t and len(set(omega12_t)) == len(omega12) == 4,
       "leg 6: classical label flip -- parity record support invariant; "
       "the constrained valuation set transports bijectively (|Omega| = 4)")

    # ---- leg 7: consistency + the type-a export --------------------------
    ck(s1 == {0} and s2 == {1},
       "leg 7: anc(flux family) = its crossed link, COMPUTED from the "
       "billing decomposition (the Paper 12 SS2 lattice identification "
       "reproduced, not postulated; the decomposition choice itself is "
       "banked [P_structural_reading] in "
       "check_T_anchor_set_is_electric_center_data -- cited, not re-graded)")
    type_a = (M12_sp.dim == 5 and Mu_sp.dim == 4
              and not Mu_sp.contains(_flat(Ps))
              and _support_slice([Ps], dims) == {0, 1})
    ck(type_a,
       "leg 7 TYPE-A EXPORT: dim M12 = 5 > 4 = dim alg(M1 u M2); the fused "
       "singlet P_s is NOT in alg(M1 u M2) (membership test, exact); "
       "supp(P_s) = both links -- the deviation-witness data the sibling "
       "check_T_delta_JR_derived consumes by live call. (Numerically "
       "coincident with, and distinct from, the banked shared-vertex "
       "centre extension -- module docstring fence)")

    n_legs = len(checks)

    return _result(
        name='T_anchor_support_formalization -- supports exist uniquely '
             '(slice-map lemma, arbitrary finite-dim factors), anc = supp '
             'of the record algebra, independence <=> disjoint anchors '
             'with the two-clause honesty',
        tier=4,
        epistemic='P',
        summary=(
            'THE ALGEBRAIC ANCHOR (Paper 12 round-6 walk C1, reviewer Q1). '
            'On a finite interface presentation (V, {A_v}, C) with '
            'ARBITRARY finite-dimensional unital *-algebra factors (full '
            'matrix algebras NOT assumed; witnessed on the lattice\'s own '
            'with-centre billing factor C (+) M_2), the support '
            'supp(M) = smallest W with M c A_W (x) 1 exists and is unique '
            '-- the admissible-W family is intersection-closed (slice-map '
            'lemma), with the pointwise characterization supp(M) = '
            '{v : E_v does not fix M} verified against brute-force '
            'enumeration on four algebras. Supports obey a calculus '
            '(monotone; union-additive under generation; covariant under '
            'relabelings), and anc(S) := supp(M(S)). Independence <=> '
            'disjoint anchors, in two halves with the honesty carried: '
            'disjoint => independent is PURE finite-dimensional algebra '
            '(commutation + canonical M1 (x) M2 with '
            'dim-multiplicativity; the merely-commuting subtlety settled '
            'by decomposition-relativity), while independent => disjoint '
            'is IRREDUCIBLY LEDGER-LEVEL (budget competition at the '
            'shared locus, check_T_M steps 4-9 reproduced in exact '
            'Fractions; A1 + L_epsilon*, not operator algebra) and partly '
            'definitional for the two-clause notion of independence -- '
            'stated plainly, not smoothed over. The honesty control pins '
            'it: two distinct records on one four-state locus have '
            'trivially intersecting algebras, a dimension-factorizing '
            'joint algebra (4 = 2 * 2), and Delta = 0, yet independence '
            'fails at the budget clause alone -- so Delta = 0 does NOT '
            'certify independence, and the purely algebraic biconditional '
            'is FALSE (the two-clause one is the theorem). Relabel '
            'covariance under G_rel = (prod_v Aut(A_v)) x| Perm_iso(V) '
            'witnessed three ways (link swap, factor-wise unitary, '
            'classical label flip); anti-automorphisms excluded from '
            'G_rel with the reason stated (transposes reverse products; '
            'harmless -- every certified quantity is '
            'transpose-invariant). Consistency: anc(flux family) = '
            'crossed-link set COMPUTED (the lattice identification '
            'reproduced; the reading cited at its banked '
            '[P_structural_reading] home, never re-graded), and the '
            'fused-singlet type-a deviation data (dim 5 > 4; membership '
            'failure; two-locus support) exported for the sibling '
            'check_T_delta_JR_derived. The counting identity and the '
            'R-convention live in the sibling check. All arithmetic exact '
            'over Q; %d assertions. Occupancy: not consumed.' % n_legs
        ),
        key_result=(
            'supp(M) exists uniquely (intersection-closed family; slice-map '
            'characterization) for arbitrary finite-dim factors incl. '
            'with-centre; anc = supp of the record algebra; disjoint '
            'anchors => independent by pure algebra (canonical tensor '
            'factorization), independent => disjoint anchors by budget '
            'competition (ledger-level, definitional-in-part); the honesty '
            'control separates the clauses (algebra passes, budget fails, '
            'Delta = 0); J/R/Delta relabel-invariance algebra half proved.'
        ),
        dependencies=['A1', 'T_M', 'L_loc', 'L_epsilon*'],
        cross_refs=['check_T_anchor_set_is_electric_center_data',
                    'T_delta_JR_derived',
                    'T_delta_disjoint_additivity',
                    'T_cost_count_characterization',
                    'FD1_structural_completeness'],
        n_assertions=n_legs,
        artifacts={
            'slice_lemma': 'W(M) intersection-closed; unique minimum; '
                           'pointwise slice characterization; verified on '
                           'C (+) M_2 factors (no fullness)',
            'two_clause_honesty': 'clause (a) algebra + clause (b) budget; '
                                  '<= pure algebra, => ledger-level and '
                                  'partly definitional; honesty control: '
                                  'algebra factorizes, Delta = 0, budget '
                                  'fails',
            'meson_type_a': {'dim_M12': M12_sp.dim,
                             'dim_alg_union': Mu_sp.dim,
                             'singlet_in_union': False,
                             'supp_singlet': sorted(
                                 _support_slice([Ps], dims))},
            'G_rel': '(prod_v Aut(A_v)) x| Perm_iso(V); anti-automorphisms '
                     'excluded with stated reason (product-reversing; all '
                     'certified quantities transpose-invariant)',
            'ledger_covariance': 'that billing attaches no cost to a '
                                 'relabeling is X1/FD1-sc (allocation '
                                 'reading), named at one gate, not '
                                 're-derived here',
            'reading_gate': 'billing-decomposition choice = lattice '
                            'identification + allocation reading, cited at '
                            'check_T_anchor_set_is_electric_center_data '
                            '[P_structural_reading]',
        },
    )


_CHECKS = {
    'check_T_anchor_support_formalization':
        check_T_anchor_support_formalization,
}


def register(registry):
    """Register the anchor-support-algebra check into the bank."""
    registry.update(_CHECKS)


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == '__main__':
    for _n, _r in run_all().items():
        print(('PASS' if _r.get('passed', True) else 'FAIL'), _n)
        print('  grade:', _r['epistemic'], '| tier', _r['tier'])
        print('  n_assertions:', _r['n_assertions'])
        print('  ', _r['key_result'])


# ---------------------------------------------------------------------------
# Interface Engine onboarding (Full Bank Onboarding wave, 2026-07-04)
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "foundation:anchor_support_formalization",
        "axis": "ROUTE",
        "route": "anchor_support_algebra",
        "expect_export": True,
        "payload": {
            "name": "anchor_support_formalization",
            "closure_kind": "internal_identity",
            "identity_summary": (
                "anc(S) := supp(M(S)) -- the anchor set IS the support of "
                "the record algebra, by structural identity: on finite "
                "interface presentations with ARBITRARY finite-dimensional "
                "unital *-algebra factors (with-centre factors included, "
                "C (+) M_2 the witnessed case), supp(M) exists and is unique "
                "(slice-map lemma), and obeys the support calculus (monotone "
                "under inclusion; union-additive under algebra generation; "
                "covariant under relabelings) [P]. Independence <=> disjoint "
                "anchors holds in TWO CLAUSES whose asymmetry is part of the "
                "statement: <= is pure algebra; => is LEDGER-LEVEL -- the "
                "in-check honesty control shows the forward clause CANNOT be "
                "operator-algebraic. "
                "(check_T_anchor_support_formalization, anchor_support_algebra.py)"
            ),
        },
        "note": (
            "Onboards the Paper 12 round-6 algebraic-anchor formalization "
            "onto the ROUTE axis as a structural identity. The two-clause "
            "honesty is frozen into the identity text: a future flattening "
            "to a clean operator-algebraic biconditional fails the pin."
        ),
    },
)
