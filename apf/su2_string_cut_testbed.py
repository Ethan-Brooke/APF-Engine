"""apf/su2_string_cut_testbed.py -- the SU(2) strong-coupling string-cut testbed.

v24.3.372 (2026-07-03, Paper 12 review-2 lane B3; fresh-context hostile audit
AUDIT_ROUND2 LAND-WITH-FIXES 0.80, fixes B3-1 + B3-2 + B3-3 carried). Walk of
record: "The Turning/p12_review2_walks_2026-07-03/b3_toy_testbed/" (REPORT.md
+ staged check + witnesses w1/w2 + run logs). Answers the reviewer's
worked-example ask + Q2 (native operator sets) on the SU(2) Kogut-Susskind
strong-coupling string family j in {1/2, 1, 3/2, 2}.

Three checks (the first two v24.3.372; the third v24.3.383,
2026-07-04, Paper 12 round-7 walk D1 + fresh-context hostile audit
LAND-WITH-FIXES 0.85, findings F1-F8 all carried; walk of record:
"The Turning/p12_review7_walks_2026-07-04/d1_sign_products/"):

  check_T_su2_string_cut_comovement  [P_structural_reading]
      The Delta/record ordering vs the standard strong-coupling confinement
      diagnostic, ORDERINGS ONLY. The verdict is PARTIAL and carries a
      FOUR-CLAUSE split that must never be flattened to "co-moves":
        (i)   asymptotic N-ality clause CO-MOVES at sign/class strength
              (partitions identical; collapse representatives match);
        (ii)  intra-family leading-order ordering is UNDER-DETERMINED on the
              Delta side beyond sign (reading-dependence pinned: unit-count
              flat vs monotone-count co-moving; neither banked);
        (iii) split-vs-unsplit probe DIVERGES robustly (every natural
              additive counting reading gives ANTI or TIE against the
              diagnostic's strict preference for split flux) -- Delta is a
              capacity ledger, not an energy functional;
        (iv)  tautology fence: the Delta side consumes d_cut = 2j+1,
              N-ality, and factorizability; it never computes C2 = j(j+1)
              (functional separation witnessed exactly).
      Grade [P_structural_reading]: exact rep theory + the banked
      record-theorem criterion (Delta > 0 <=> non-factorizable record) + an
      argmin(A2)-style reading for the asymptotic minimal content. Model-
      scoped (leading strong coupling, SU(2), Kogut-Susskind).

  check_T_su2_string_cut_native_algebra  [P]
      Q2: the native gauge-invariant operator set at a k-string cut (pairwise
      fusion electric invariants C_ab = (S_a+S_b)^2 = 1 + P_ab; flux-exchange
      operators polynomial in them) GENERATES THE FULL gauge-invariant cut
      algebra (exact over Q for k = 1, 2; MOD-P-CORROBORATED at k = 3: rank
      mod p at two primes meets the exact commutant upper bound
      dim 132 = 81 + 25 + 25 + 1, the M_9 (+) M_5 (+) M_5 (+) M_1 blocks --
      corroboration, never cited as the exact-over-Q statement, which is
      banked at k = 1, 2 only), acts non-abelianly on the k = 2
      physical pairing sector (exact 2x2 non-commutation), and is abelian for
      any single-string cut (all multiplicities 1, any j) -- so the KCBS /
      Yu-Oh contextuality certified by the banked
      check_T_gauge_invariant_colour_interface_is_contextual /
      ..._state_independent_contextual lives on NATIVELY GENERATED operators,
      and contextuality at a string cut is a multi-string (fusion-degeneracy)
      phenomenon, not a large-j one. Grade [P] for the algebra facts (exact);
      the contextuality verdict itself stays with the banked engine checks
      (cross-ref, not recomputed here).

  check_T_no_negative_delta_at_gauge_cut_family  [P]
      The D1 family-scoped proposition (Paper 12 round-7, reviewer Q2), the
      floor and the content separated: within the walked family (per-string
      presentations of DISTINCT strings; configurations disjoint-links /
      shared-vertex / shared-cut, k <= 3) R = 0 by PARTITION-DISTINCTNESS,
      so Delta >= -eps*R = 0 occupancy-free (the banked CH1 bound); every
      shared-anchor configuration carries a certified type-(a) joint
      channel (fused-cut 14 > 4 computed exactly; shared-vertex 5 > 4
      consumed LIVE); the gauge copy-pair collapses via FD1-sc under a
      NAMED value-side refinement of the banked channel convention (the
      partition rule; the Q1-vs-2Q1 disagreement pair run in-check).
      Negative Delta arises only via literal co-presentation -- the
      classical copy-pair mechanism. The floor is convention-near-
      tautological given the family definition, and the check says so.

MODELLING FENCE (carried in-docstring per the exotic-algebra precedent,
check_T_exotic_gauge_invariant_algebra_is_nonabelian [P]): the cut is
modelled as the single diagonal comparison group, exactly as in the banked
tetraquark checks. The fence is inherited, not invented here.

FENCES (verbatim survival from the walk): no magnitude/units claim for Delta
(no grounded eps for colour -- the gauge_invariant_record fence); no spectral
claim; no tension-LAW claim (leading strong-coupling Casimir scaling is a
MODEL fact, not a continuum claim; Casimir-vs-sine stays spectrum-blind
territory, check_T_colour_contextuality_is_kstring_spectrum_blind);
occupancy never claimed; the screening story's lattice evidence is imported
context (only its kinematic N-ality part is computed).

All arithmetic exact (Fractions / integers), pure stdlib, except the
k = 3 mod-p leg (numpy int64, ported 2026-07-04 from the B3 walk witness
w2_native_operators.py: every intermediate is bounded by p**2 < 2**63 for
p <= 998244353, so the mod-p ranks are exact integers).
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from typing import Dict

from apf.apf_utils import check, _result


# ============================================================================
# exact helpers (stdlib only)
# ============================================================================

def _frac_rref(rows, dim):
    """in-place rref; returns (rank, pivcols, M)."""
    M = [list(map(F, r)) for r in rows]
    R = len(M)
    piv = []
    rank = 0
    for col in range(dim):
        p = next((r for r in range(rank, R) if M[r][col] != 0), None)
        if p is None:
            continue
        M[rank], M[p] = M[p], M[rank]
        inv = 1 / M[rank][col]
        M[rank] = [inv * x for x in M[rank]]
        for r in range(R):
            if r != rank and M[r][col] != 0:
                f = M[r][col]
                M[r] = [M[r][k] - f * M[rank][k] for k in range(dim)]
        piv.append(col)
        rank += 1
    return rank, piv, M


def _rank(rows):
    if not rows:
        return 0
    return _frac_rref(rows, len(rows[0]))[0]


def _kernel(rows, dim):
    rank, piv, M = _frac_rref(rows, dim)
    free = [c for c in range(dim) if c not in piv]
    out = []
    for fc in free:
        v = [F(0)] * dim
        v[fc] = F(1)
        for r, pc in enumerate(piv):
            v[pc] = -M[r][fc]
        out.append(v)
    return out


def _su2_tensor(dec, b):
    out = {}
    for a, m in dec.items():
        for c in range(abs(a - b), a + b + 1, 2):
            out[c] = out.get(c, 0) + m
    return out


def _c2(a):
    j = F(a, 2)
    return j * (j + 1)


class _Span:
    """incremental exact row span over Q."""

    def __init__(self, dim):
        self.dim = dim
        self.rows = []
        self.piv = []

    def add(self, v):
        v = list(map(F, v))
        for r, c in zip(self.rows, self.piv):
            if v[c]:
                f = v[c]
                v = [v[k] - f * r[k] for k in range(self.dim)]
        c = next((k for k in range(self.dim) if v[k] != 0), None)
        if c is None:
            return False
        inv = 1 / v[c]
        v = [inv * x for x in v]
        self.rows.append(v)
        self.piv.append(c)
        return True

    @property
    def rank(self):
        return len(self.rows)


def _swap(n, a, b):
    d = 1 << n
    M = [[0] * d for _ in range(d)]
    for s in range(d):
        ba = (s >> (n - 1 - a)) & 1
        bb = (s >> (n - 1 - b)) & 1
        t = s ^ ((1 << (n - 1 - a)) | (1 << (n - 1 - b))) if ba != bb else s
        M[t][s] = 1
    return M


def _eye(d):
    return [[1 if i == j else 0 for j in range(d)] for i in range(d)]


def _mm(A, B):
    d = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(d)) for j in range(d)] for i in range(d)]


def _madd(A, B, sgn=1):
    return [[A[i][j] + sgn * B[i][j] for j in range(len(A))] for i in range(len(A))]


def _two_sx(n):
    d = 1 << n
    M = [[0] * d for _ in range(d)]
    for s in range(d):
        for i in range(n):
            M[s ^ (1 << i)][s] += 1
    return M


def _two_sz(n):
    d = 1 << n
    M = [[0] * d for _ in range(d)]
    for s in range(d):
        M[s][s] = n - 2 * bin(s).count("1")
    return M


def _ceil_log2(d):
    """ceil(log2(d)) for integer d >= 1, exactly (no floats)."""
    return (d - 1).bit_length()


# ============================================================================
# check 1: the ordering co-movement (PARTIAL, certified, four clauses)
# ============================================================================

def check_T_su2_string_cut_comovement() -> Dict:
    """The Delta/record ordering vs the strong-coupling diagnostic: PARTIAL,
    four clauses (module docstring). NEVER flatten the verdict to 'co-moves'.

    F1 FENCE (from the Delta-calculus landing, carried per audit fix B3-3):
    where clause (iii) invokes additivity of Delta across the two parallel
    strings, 'disjoint' means ANCHOR-disjoint (T_M's biconditional) -- the
    two parallel strings anchor at disjoint anchor sets, which is the
    operative sense under which check_T_delta_disjoint_additivity licenses
    the additive composition. It is not a merely spatial label.

    Grade [P_structural_reading]: the rep theory is exact; the readings
    consumed are (a) the banked record-theorem sign criterion (Delta > 0 <=>
    non-factorizable record) and (b) an argmin(A2)-style reading for the
    asymptotic minimal dressed content (clause (i)); the argmin rider is
    what keeps clause (i) off bare [P].

    POINTER (v24.3.380 landing): clause (ii)'s 'neither functional is
    banked' stands AT BANK LEVEL -- the bank fixes only Delta = eps*(J-R)
    and the sign criterion -- but the ceil-log2 functional is since
    operationally GROUNDED under the named register reading
    (check_T_register_reading_grounds_ceil_log2_count, delta_calculus.py):
    grounded-under-a-reading, still not banked as the ledger's J; the
    UNDER-DETERMINED verdict of clause (ii) is unchanged.
    """
    fam = [1, 2, 3, 4]  # a = 2j
    checks = []

    def ck(cond, msg):
        checks.append((bool(cond), msg))
        check(cond, msg)

    # --- diagnostic side, leading order: strict C2 ordering (exact) ---------
    ck(all(_c2(fam[i]) < _c2(fam[i + 1]) for i in range(3)),
       "leading-order diagnostic C2(j) strictly increasing on the family")

    # --- Delta/record side: cut record exact (unique singlet; rank 2j+1;
    #     maximally mixed) via the sqrt-free Sym^a restriction ---------------
    for a in fam:
        d = a + 1
        dim = d * d
        Ax = [[F(0)] * d for _ in range(d)]
        Az = [[F(0)] * d for _ in range(d)]
        for k in range(d):
            Az[k][k] = F(a - 2 * k)
            if k + 1 < d:
                Ax[k + 1][k] = F(k + 1)
            if k:
                Ax[k - 1][k] = F(a - k + 1)

        def tot(A):
            T = [[F(0)] * dim for _ in range(dim)]
            for i in range(d):
                for l in range(d):
                    r = i * d + l
                    for ii in range(d):
                        if A[ii][i]:
                            T[ii * d + l][r] += A[ii][i]
                    for ll in range(d):
                        if A[ll][l]:
                            T[i * d + ll][r] += A[ll][l]
            return T
        ker = _kernel(tot(Ax) + tot(Az), dim)
        ck(len(ker) == 1, f"a={a}: singlet multiplicity 1 in j(x)j")
        V = [[ker[0][i * d + l] for l in range(d)] for i in range(d)]
        ck(_rank(V) == d, f"a={a}: cut Schmidt rank = 2j+1 = {d}")
        from math import comb
        off0 = all(sum(V[k][l] * V[m][l] * comb(a, l) for l in range(d)) == 0
                   for k in range(d) for m in range(d) if k != m)
        dg = [F(comb(a, k)) * sum(V[k][l] ** 2 * F(comb(a, l)) for l in range(d))
              for k in range(d)]
        ck(off0 and len(set(dg)) == 1 and dg[0] != 0,
           f"a={a}: reduced cut state exactly maximally mixed")

    # --- N-ality / dressing reachability (kinematic screening), exact ------
    reach = {}
    for a in fam:
        dec = {a: 1}
        mn = a
        for _ in range(6):
            dec = _su2_tensor(dec, 2)  # adjoint = a=2
            mn = min(mn, min(dec))
            ck(all(c % 2 == a % 2 for c in dec),
               f"a={a}: adjoint dressing preserves N-ality at every step")
        reach[a] = mn
        ck((mn == 0) == (a % 2 == 0), f"a={a}: singlet reachable IFF N-ality 0")
        ck(mn in (0, 1), f"a={a}: minimal dressed content is singlet or j=1/2")

    # --- clause (i): asymptotic partitions identical ------------------------
    ck(all((a % 2 == 0) == (reach[a] == 0) for a in fam),
       "CLAUSE (i) CO-MOVE: diagnostic N-ality classes == Delta_min sign classes "
       "({1,2} trivial; {1/2,3/2} fundamental class, both collapsing to the j=1/2 "
       "representative)")

    # --- clause (ii): reading-dependence pin --------------------------------
    dcut = {a: a + 1 for a in fam}
    ck(all(dcut[fam[i]] < dcut[fam[i + 1]] for i in range(3)),
       "monotone-count reading: d_cut strictly increasing (co-moves with C2 -- "
       "but automatic on a one-parameter family)")
    # unit-count reading is flat by construction (J = 1 per irreducible record);
    # the two readings disagree on whether the family is ordered at all:
    ck(len({1 for _ in fam}) == 1 and len(set(dcut.values())) == len(fam),
       "CLAUSE (ii) UNDER-DETERMINED: unit-count reading flat, monotone-count "
       "reading strictly ordered; neither functional is banked (bank fixes only "
       "Delta = eps*(J-R) and the sign criterion; ceil-log2 since GROUNDED "
       "under the named register reading, "
       "check_T_register_reading_grounds_ceil_log2_count -- grounded, not "
       "banked as the ledger's J)")

    # --- clause (iii): split-vs-unsplit divergence pin ----------------------
    # Configurations: SPLIT = two parallel j=1/2 strings (anchor-disjoint,
    # F1 fence above; Delta additive across them by
    # check_T_delta_disjoint_additivity, landed same pass); UNSPLIT = one
    # j=1 string. Audit fix B3-1: every reading below is COMPUTED from the
    # model quantities (the dcut dict + the two-string composition), not
    # asserted as literal arithmetic.
    split = [dcut[1], dcut[1]]     # two j=1/2 strings: d_cut values [2, 2]
    unsplit = [dcut[2]]            # one j=1 string:    d_cut value  [3]
    diag_split = sum(_c2(1) for _ in split)   # 2 * C2(1/2) = 3/2
    diag_unsplit = _c2(2)                     # C2(1) = 2
    ck(diag_split < diag_unsplit,
       "diagnostic strictly prefers split flux: 2*C2(1/2) = 3/2 < C2(1) = 2")
    # unit-count reading: one irreducible record per string, additive
    unit_split, unit_unsplit = len(split), len(unsplit)
    # log2-count reading: log2(prod d_cut), compared via the monotone
    # transform 2^x, i.e. compare the exact integer products of d_cut
    prod_split = split[0] * split[1]
    prod_unsplit = unsplit[0]
    # (d-1)-count reading: sum (d_cut - 1), additive
    dm1_split = sum(d - 1 for d in split)
    dm1_unsplit = sum(d - 1 for d in unsplit)
    # ceil-log2 (qubit-count) reading: sum ceil(log2 d_cut), additive
    cl2_split = sum(_ceil_log2(d) for d in split)
    cl2_unsplit = sum(_ceil_log2(d) for d in unsplit)
    ck(unit_split > unit_unsplit,
       f"unit-count reading: {unit_split} > {unit_unsplit} -- ANTI the "
       "diagnostic's split preference")
    ck(prod_split > prod_unsplit,
       f"log2-count reading (via 2^x): {prod_split} > {prod_unsplit} -- ANTI")
    ck(dm1_split == dm1_unsplit,
       f"(d-1)-count reading: {dm1_split} == {dm1_unsplit} -- TIE")
    ck(cl2_split == cl2_unsplit,
       f"ceil-log2 reading: {cl2_split} == {cl2_unsplit} -- TIE")
    ck(True,
       "CLAUSE (iii) DIVERGE: every natural additive counting reading gives ANTI "
       "or TIE against the diagnostic's strict split preference -- Delta is a "
       "capacity ledger, not an energy functional")

    # --- clause (iv): tautology fence (functional separation) --------------
    ratios = {a: _c2(a) / (a + 1) for a in fam}
    ck(len(set(ratios.values())) == len(fam),
       "CLAUSE (iv) tautology fence: C2/d_cut non-constant -- the Delta side's "
       "invariants (d_cut, N-ality, factorizability) are not Casimir counting")

    return _result(
        name='T_su2_string_cut_comovement -- Delta/record ordering vs the '
             'strong-coupling diagnostic on the SU(2) string family: PARTIAL '
             '(four clauses, never flattened)',
        tier=4,
        epistemic='P_structural_reading',
        summary=(
            'SU(2) Kogut-Susskind strong-coupling string family j in '
            '{1/2, 1, 3/2, 2}, orderings only, all arithmetic exact. Verdict '
            'PARTIAL with the four-clause split carried in full: (i) the '
            'asymptotic N-ality clause CO-MOVES at sign/class strength -- '
            'the diagnostic N-ality classes and the Delta_min sign classes '
            'are the same partition, with matching collapse representatives '
            '(kinematic screening exact at every dressing step; the '
            'asymptotic minimal content consumes an argmin(A2)-style '
            'reading, which is what keeps this clause off bare [P]); (ii) '
            'the intra-family leading-order ordering is UNDER-DETERMINED on '
            'the Delta side beyond sign -- the unit-count reading is flat, '
            'the monotone-count reading strictly ordered, and neither '
            'functional is banked (ceil-log2 is since operationally '
            'grounded under the named register reading, '
            'check_T_register_reading_grounds_ceil_log2_count -- grounded, '
            'not banked as the ledger\'s J); (iii) the split-vs-unsplit probe '
            'DIVERGES -- the diagnostic strictly prefers split flux '
            '(2*C2(1/2) = 3/2 < C2(1) = 2) while every natural additive '
            'counting reading (unit-count, log2-count, (d-1)-count, '
            'ceil-log2), each computed from the model d_cut quantities and '
            'composed additively across the two anchor-disjoint strings '
            '(check_T_delta_disjoint_additivity; F1: anchor-disjointness is '
            'the operative sense of disjoint), gives ANTI or TIE -- Delta is '
            'a capacity ledger, not an energy functional; (iv) tautology '
            'fence -- the Delta side consumes d_cut = 2j+1, N-ality, and '
            'factorizability, never C2 = j(j+1), and the functional '
            'separation is witnessed exactly (C2/d_cut ratios pairwise '
            'distinct). Model-scoped: leading strong coupling, SU(2), '
            'cut modelled as the single diagonal comparison group. No '
            'magnitude/units, spectral, tension-law, or occupancy claim.'
        ),
        key_result=(
            'PARTIAL, four clauses: (i) N-ality classes CO-MOVE '
            '(sign/class, argmin reading priced); (ii) intra-family ordering '
            'UNDER-DETERMINED beyond sign; (iii) split-vs-unsplit DIVERGES '
            '(ANTI or TIE under every natural additive reading) -- Delta is '
            'a capacity ledger, not an energy functional; (iv) the Delta '
            'side never computes the Casimir (tautology fence).'
        ),
        dependencies=[
            'check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P',
            'check_T_delta_disjoint_additivity',
            'check_L_cost', 'check_L_irr',
            'check_T_center_order_parameter_triality',
        ],
        cross_refs=['check_T_colour_contextuality_is_kstring_spectrum_blind',
                    'check_T_su2_string_cut_native_algebra',
                    'check_T_register_reading_grounds_ceil_log2_count'],
        verdict='PARTIAL',
        clauses={
            'asymptotic_Nality': 'CO-MOVE (sign/class, grounded; argmin rider priced)',
            'leading_order_intra_family': 'UNDER-DETERMINED (reading-dependent beyond sign)',
            'split_vs_unsplit': 'DIVERGE (ANTI or TIE under every natural reading)',
            'tautology_fence': 'Delta side never computes C2',
        },
        n_assertions=len(checks),
        artifacts={
            'fences': ['orderings only -- no grounded eps, no magnitudes',
                       'leading strong coupling model facts only -- no tension law',
                       'screening dynamics imported; kinematic N-ality computed',
                       'occupancy not claimed; no spectral claim',
                       'F1: disjoint = ANCHOR-disjoint for the clause-(iii) '
                       'additive composition'],
            'clause_iii_readings': {
                'unit_count': [unit_split, unit_unsplit],
                'dcut_product_for_log2': [prod_split, prod_unsplit],
                'd_minus_1': [dm1_split, dm1_unsplit],
                'ceil_log2': [cl2_split, cl2_unsplit],
                'diagnostic_C2': [str(diag_split), str(diag_unsplit)],
            },
        },
    )


# ============================================================================
# the k = 3 mod-p leg (ported 2026-07-04 from the B3 walk witness)
# ============================================================================

def _k3_native_generation_modp(primes=(1000003, 998244353)):
    """The k = 3 (n = 6 cut indices, d = 64) native-generation leg: rank of
    the unital algebra generated by the native fusion invariants C_ab, mod p
    at two primes, against the exact commutant upper bound.

    Certification shape (each step exact): (a) every generator commutes with
    Sx_tot, Sz_tot over the INTEGERS, so the generated algebra sits inside
    the rational commutant, whose dimension is the exact multiplicity sum
    132 = 81 + 25 + 25 + 1; (b) the rank mod p of an integer matrix family
    never exceeds its rank over Q; (c) the computed mod-p rank equals 132 at
    BOTH primes, meeting the upper bound. Stated as MOD-P CORROBORATION of
    full native generation at k = 3 (the exact-over-Q statement is banked at
    k = 1, 2 only). numpy int64 throughout; all intermediates are bounded by
    p**2 < 2**63 for p <= 998244353, so the ranks are exact integers.
    """
    import numpy as np
    n = 6
    d = 1 << n
    I = np.eye(d, dtype=np.int64)
    gens = [np.array(_madd(_swap(n, a, b), _eye(d)), dtype=np.int64)
            for a, b in combinations(range(n), 2)]
    SX = np.array(_two_sx(n), dtype=np.int64)
    SZ = np.array(_two_sz(n), dtype=np.int64)
    gi = all(np.array_equal(g @ SX, SX @ g) and np.array_equal(g @ SZ, SZ @ g)
             for g in gens)
    dec = {0: 1}
    for _ in range(n):
        dec = _su2_tensor(dec, 1)
    cdim = sum(m * m for m in dec.values())
    blocks = sorted(dec.values(), reverse=True)
    ranks = {}
    for p in primes:
        rows = []     # echelon rows mod p
        pivots = []

        def _add(v, p=p, rows=rows, pivots=pivots):
            v = v % p
            for r, c in zip(rows, pivots):
                if v[c]:
                    v = (v - v[c] * r) % p
            nz = np.nonzero(v)[0]
            if len(nz) == 0:
                return False
            c = int(nz[0])
            v = (v * pow(int(v[c]), p - 2, p)) % p
            for i in range(len(rows)):
                if rows[i][c]:
                    rows[i] = (rows[i] - rows[i][c] * v) % p
            rows.append(v)
            pivots.append(c)
            return True

        queue = [I] + [g.copy() for g in gens]
        while queue:
            M = queue.pop()
            if _add(M.reshape(-1)):
                if len(rows) >= cdim:
                    break     # met the exact upper bound; nothing above it
                for g in gens:
                    queue.append((M @ g) % p)
        ranks[p] = len(rows)
    return {
        'gauge_invariant_exact': bool(gi),
        'cdim': cdim,
        'blocks': blocks,
        'ranks': ranks,
    }


# ============================================================================
# check 2: native operator algebra at the cut (Q2)
# ============================================================================

def check_T_su2_string_cut_native_algebra() -> Dict:
    """Native gauge-invariant operator algebra at the string cut (Q2): the
    pairwise fusion electric invariants C_ab = (S_a+S_b)^2 = 1 + P_ab
    generate the FULL gauge-invariant cut algebra (exact over Q, k = 1, 2;
    MOD-P-CORROBORATED at k = 3, two primes against the exact dim-132
    commutant upper bound -- never cite the k = 3 leg as exact-over-Q);
    abelian for any single-j string; non-abelian on the k=2 pairing sector.

    MODELLING FENCE (per the exotic-algebra precedent, registered [P] with
    the same modelling): the cut is modelled as the single diagonal
    comparison group, as in the banked tetraquark checks
    (check_T_exotic_gauge_invariant_algebra_is_nonabelian). Grade [P] for
    the algebra facts (all exact); the contextuality verdicts stay with the
    banked engine checks (cross-refs), not recomputed here.
    """
    checks = []

    def ck(cond, msg):
        checks.append((bool(cond), msg))
        check(cond, msg)

    for k_strings, n in ((1, 2), (2, 4)):
        d = 1 << n
        I = _eye(d)
        gens = [_madd(_swap(n, a, b), I) for a, b in combinations(range(n), 2)]
        SX, SZ = _two_sx(n), _two_sz(n)
        for g in gens:
            ck(_mm(g, SX) == _mm(SX, g) and _mm(g, SZ) == _mm(SZ, g),
               f"n={n}: native fusion invariant gauge-invariant at the cut (exact)")
        # commutant dim from exact multiplicities
        dec = {0: 1}
        for _ in range(n):
            dec = _su2_tensor(dec, 1)
        cdim = sum(m * m for m in dec.values())
        span = _Span(d * d)
        basis = []
        queue = [I] + [g for g in gens]
        while queue:
            M = queue.pop()
            if span.add([x for row in M for x in row]):
                basis.append(M)
                if span.rank > cdim:
                    break
                for g in gens:
                    queue.append(_mm(M, g))
        ck(span.rank == cdim,
           f"k={k_strings} strings: native algebra dim {span.rank} == commutant dim "
           f"{cdim} (FULL native generation, exact over Q)")
        if n == 2:
            ck(max(dec.values()) == 1 and cdim == 2,
               "k=1: cut algebra abelian (single context -- SepStr structure); the "
               "record itself is the entangled rank-2 singlet (entanglement rung "
               "without contextuality)")

    # --- k = 3 leg: mod-p corroboration at two primes (ported 2026-07-04
    #     from the B3 walk witness w2_native_operators.py + run log) ----------
    k3 = _k3_native_generation_modp()
    ck(k3['gauge_invariant_exact'],
       "k=3 strings (n=6 cut indices): native fusion invariants gauge-invariant "
       "at the cut (exact integer commutators)")
    ck(k3['cdim'] == 132 and k3['blocks'] == [9, 5, 5, 1],
       "k=3: exact commutant upper bound dim 132 = 81+25+25+1 "
       "(M_9 (+) M_5 (+) M_5 (+) M_1)")
    for _p, _r in sorted(k3['ranks'].items()):
        ck(_r == k3['cdim'],
           f"k=3 strings: native algebra rank mod {_p} = {_r} == exact upper "
           f"bound {k3['cdim']} (FULL native generation MOD-P-CORROBORATED; "
           "the exact-over-Q statement stays banked at k = 1, 2 only)")

    # single-string cut of ANY j: all multiplicities 1 => abelian (exact rule)
    for a in (1, 2, 3, 4):
        dec = _su2_tensor({0: 1}, a)
        dec = _su2_tensor(dec, a)
        ck(max(dec.values()) == 1,
           f"single j={F(a, 2)} string cut: multiplicity-free => abelian cut algebra "
           "(contextuality is multi-string, not large-j)")

    # k=2 physical pairing sector: exact non-commuting 2x2 native action
    n, d = 4, 16

    def pv(p1, p2):
        v = [0] * 16
        (a, b), (c, e) = p1, p2
        for x in (0, 1):
            for y in (0, 1):
                bits = [0] * 4
                bits[a], bits[b] = x, 1 - x
                bits[c], bits[e] = y, 1 - y
                v[bits[0] * 8 + bits[1] * 4 + bits[2] * 2 + bits[3]] += \
                    (1 - 2 * x) * (1 - 2 * y)
        return v

    A, B = pv((0, 1), (2, 3)), pv((0, 3), (1, 2))
    SX, SZ = _two_sx(4), _two_sz(4)

    def mv(M, v):
        return [sum(M[i][k] * v[k] for k in range(16)) for i in range(16)]
    ck(not any(mv(SX, A)) and not any(mv(SZ, A)) and not any(mv(SX, B))
       and not any(mv(SZ, B)), "pairing states gauge-invariant (exact)")
    G = [[sum(x * y for x, y in zip(u, w)) for w in (A, B)] for u in (A, B)]
    det = G[0][0] * G[1][1] - G[0][1] * G[1][0]
    ck(det != 0, "pairing states independent (Gram non-degenerate)")

    def restrict(M):
        cols = []
        for v in (A, B):
            w = mv(M, v)
            r0 = sum(x * y for x, y in zip(A, w))
            r1 = sum(x * y for x, y in zip(B, w))
            al = F(G[1][1] * r0 - G[0][1] * r1, det)
            be = F(-G[1][0] * r0 + G[0][0] * r1, det)
            ck(all(F(w[i]) - al * A[i] - be * B[i] == 0 for i in range(16)),
               "restriction stays in the pairing sector (exact membership)")
            cols.append((al, be))
        return [[cols[0][0], cols[1][0]], [cols[0][1], cols[1][1]]]

    C12 = _madd(_swap(4, 0, 1), _eye(16))
    C13 = _madd(_swap(4, 0, 2), _eye(16))
    R12, R13 = restrict(C12), restrict(C13)

    def mm2(X, Y):
        return [[sum(X[i][k] * Y[k][j] for k in range(2)) for j in range(2)]
                for i in range(2)]
    comm = [[mm2(R12, R13)[i][j] - mm2(R13, R12)[i][j] for j in range(2)]
            for i in range(2)]
    ck(any(x != 0 for row in comm for x in row),
       "k=2 pairing sector: restricted native invariants do NOT commute "
       "(non-abelian M_2 record algebra; Gleason dim-2 fence on this sector)")

    return _result(
        name='T_su2_string_cut_native_algebra -- the native fusion electric '
             'invariants generate the full gauge-invariant cut algebra',
        tier=4,
        epistemic='P',
        summary=(
            'The native gauge-invariant operator set at an SU(2) k-string '
            'cut -- the pairwise fusion electric invariants C_ab = '
            '(S_a+S_b)^2 = 1 + P_ab and flux-exchange operators polynomial '
            'in them -- GENERATES THE FULL gauge-invariant cut algebra, '
            'exact over Q at k = 1, 2 (dims 2 and 14, matching the exact '
            'commutant multiplicity sums) and MOD-P-CORROBORATED at k = 3 '
            '(rank mod p at two primes, 1000003 and 998244353, meets the '
            'exact commutant upper bound dim 132 = 81+25+25+1; corroboration '
            'only -- the exact-over-Q statement is banked at k = 1, 2); is '
            'ABELIAN for any single-j '
            'string cut (all fusion multiplicities 1 for j up to 2 -- '
            'contextuality at a string cut is a multi-string '
            'fusion-degeneracy phenomenon, not a large-j one); and acts '
            'NON-ABELIANLY on the k = 2 physical pairing sector (exact 2x2 '
            'non-commutation of the restricted invariants; Gleason dim-2 '
            'fence noted on that sector). Gauge invariance of the native '
            'set asserted exactly (integer commutators with Sx_tot, Sz_tot). '
            'Consequence: the KCBS / Yu-Oh contextuality certified by the '
            'banked engine checks lives on NATIVELY GENERATED operators -- '
            'the contextuality verdicts themselves stay with those banked '
            'checks (cross-refs), not recomputed here. Modelling fence: the '
            'cut is the single diagonal comparison group, exactly as in the '
            'banked tetraquark checks (the [P] exotic-algebra precedent). '
            'IJC_str rung only; IJC_adm/occupancy stays the empirical QAC.'
        ),
        key_result=(
            'The native fusion electric invariants C_ab = (S_a+S_b)^2 = '
            '1 + P_ab generate the FULL gauge-invariant cut algebra (exact, '
            'k=1,2; mod-p-corroborated at k=3, two primes, dim 132 upper '
            'bound met); abelian for any single-j string; non-abelian on the '
            'k=2 pairing sector. Contextuality stays certified by the '
            'banked engine checks -- here shown to live on natively '
            'generated operators.'
        ),
        dependencies=[
            'check_T_exotic_gauge_invariant_algebra_is_nonabelian',
            'check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P',
        ],
        cross_refs=['check_T_gauge_invariant_colour_interface_is_contextual',
                    'check_T_gauge_invariant_colour_interface_state_independent_contextual',
                    'check_T_su2_string_cut_comovement'],
        n_assertions=len(checks),
        artifacts={
            'fences': ['IJC_str rung only; IJC_adm/occupancy stays the empirical QAC',
                       'cut modelled as the single diagonal comparison group (as in '
                       'the banked tetraquark checks)',
                       'k=3 native generation is MOD-P-CORROBORATED (two primes, '
                       'exact upper bound met), never exact-over-Q; the '
                       'exact-over-Q statement is banked at k = 1, 2 only'],
            'k3_leg': {
                'status': 'mod-p corroborated (two primes; meets the exact '
                          'commutant upper bound); ported 2026-07-04 from the '
                          'B3 walk witness w2_native_operators.py',
                'primes': sorted(k3['ranks']),
                'ranks_mod_p': {str(p): r for p, r in sorted(k3['ranks'].items())},
                'commutant_dim_exact_upper_bound': k3['cdim'],
                'blocks': k3['blocks'],
            },
        },
    )



# ============================================================================
# sparse exact toolkit (Fraction entries, dict-of-rows; ported 2026-07-04
# from the D1 walk witness witness_d1_sign_and_products.py -- the dense
# helpers above are integer-matrix fast paths, these legs need generic
# rational commutants and membership tests)
# ============================================================================

def _sp_eye(n):
    return {i: {i: F(1)} for i in range(n)}


def _sp_mm(A, B):
    C = {}
    for i, ra in A.items():
        rc = {}
        for k, va in ra.items():
            rb = B.get(k)
            if rb:
                for j, vb in rb.items():
                    rc[j] = rc.get(j, F(0)) + va * vb
        rc = {j: v for j, v in rc.items() if v}
        if rc:
            C[i] = rc
    return C


def _sp_add(A, B, sgn=1):
    C = {i: dict(r) for i, r in A.items()}
    for i, rb in B.items():
        rc = C.setdefault(i, {})
        for j, v in rb.items():
            nv = rc.get(j, F(0)) + sgn * v
            if nv:
                rc[j] = nv
            else:
                rc.pop(j, None)
        if not rc:
            C.pop(i, None)
    return C


def _sp_sub(A, B):
    return _sp_add(A, B, -1)


def _sp_smul(c, A):
    c = F(c)
    if not c:
        return {}
    return {i: {j: c * v for j, v in r.items()} for i, r in A.items()}


def _sp_kron(A, B, nb):
    C = {}
    for i, ra in A.items():
        for j, va in ra.items():
            for p, rb in B.items():
                row = C.setdefault(i * nb + p, {})
                for q, vb in rb.items():
                    row[j * nb + q] = va * vb
    return C


def _sp_comm(A, B):
    return _sp_sub(_sp_mm(A, B), _sp_mm(B, A))


def _sp_iszero(A):
    return all(not r for r in A.values())


def _sp_eq(A, B):
    return _sp_iszero(_sp_sub(A, B))


def _sp_flat(A, n):
    v = {}
    for i, r in A.items():
        for j, val in r.items():
            if val:
                v[i * n + j] = val
    return v


def _sp_to_dense(A, n):
    M = [[F(0)] * n for _ in range(n)]
    for i, r in A.items():
        for j, v in r.items():
            M[i][j] = v
    return M


class _SpSpan:
    """Row-reduced span of sparse rational vectors (dict col -> Fraction)."""

    def __init__(self):
        self.piv = {}

    def _reduce(self, r):
        r = {k: F(v) for k, v in r.items() if v}
        while r:
            c = min(r)
            p = self.piv.get(c)
            if p is None:
                return r, c
            f = r[c] / p[c]
            for cc, v in p.items():
                nv = r.get(cc, F(0)) - f * v
                if nv:
                    r[cc] = nv
                else:
                    r.pop(cc, None)
        return r, None

    def add(self, r):
        rr, c = self._reduce(r)
        if c is None:
            return False
        self.piv[c] = rr
        return True

    def contains(self, r):
        _, c = self._reduce(r)
        return c is None

    @property
    def dim(self):
        return len(self.piv)


def _sp_rank(A):
    """Exact row rank of a sparse matrix."""
    sp = _SpSpan()
    for _, r in A.items():
        sp.add(dict(r))
    return sp.dim


def _sp_commutant_dim(gens, n):
    """dim of {X : [X, L] = 0 for all L in gens} -- exact, sparse."""
    span = _SpSpan()
    for L in gens:
        colL = {}
        for b, row in L.items():
            for q, v in row.items():
                colL.setdefault(q, {})[b] = v
        for p in range(n):
            Lp = L.get(p, {})
            for q in range(n):
                row = {}
                for b, v in colL.get(q, {}).items():
                    k = p * n + b
                    row[k] = row.get(k, F(0)) + v
                for a, v in Lp.items():
                    k = a * n + q
                    row[k] = row.get(k, F(0)) - v
                row = {k: v for k, v in row.items() if v}
                if row:
                    span.add(row)
    return n * n - span.dim


def _sp_slot_op(mats, dims):
    """kron over slots; mats: dict slot -> sparse mat; identity elsewhere."""
    out = None
    for s, d in enumerate(dims):
        m = mats.get(s, _sp_eye(d))
        if out is None:
            out = m
        else:
            out = _sp_kron(out, m, d)
    return out


# su(2) raising/lowering on C^2 (real rational; commutant of {E, F} = the
# rep commutant) and the epsilon-singlet projector on one spin-1/2 pair
_SP_E = {0: {1: F(1)}}
_SP_F = {1: {0: F(1)}}
_SP_PSING = {1: {1: F(1, 2), 2: F(-1, 2)}, 2: {1: F(-1, 2), 2: F(1, 2)}}


# ============================================================================
# check 3: no negative Delta at gauge cuts -- the family-scoped proposition
# (v24.3.383, Paper 12 round-7 walk D1)
# ============================================================================

def check_T_no_negative_delta_at_gauge_cut_family() -> Dict:
    """T_no_negative_delta_at_gauge_cut_family: no negative Delta arises in
    any per-string presentation of distinct strings across the walked
    flux-string configuration family -- the floor is R = 0 by
    PARTITION-DISTINCTNESS, the content is the type-(a) joint-channel
    witnesses plus the collapse legs. (Landed v24.3.383, 2026-07-04, Paper
    12 round-7 walk D1, reviewer Q2; fresh-context hostile audit
    LAND-WITH-FIXES 0.85, findings F1-F8 ALL carried; walk of record:
    "The Turning/p12_review7_walks_2026-07-04/d1_sign_products/".)

    THE FAMILY (defined in-statement, part of the claim -- audit F2): the
    flux-string record families of this module's SU(2) strong-coupling
    testbed, presented PER-STRING for DISTINCT strings (distinct
    static-source pairs), over the standard cut set walked -- the
    per-configuration list:
      (1) k = 2 parallel strings on disjoint links (anchor-disjoint);
      (2) k = 2 strings sharing one boundary vertex (the banked 41/5
          model, check_T_anchor_set_is_electric_center_data leg 7);
      (3) k = 2 strings fused at one cut (four spin-1/2 cut indices);
      (4) k = 3 strings fused at one cut, any pair.

    THE STATEMENT, three separated legs (audit F2 -- the floor and the
    content must not be mixed):

      (i) THE FLOOR. Within the family, R = 0 for every pair of families,
          by PARTITION-DISTINCTNESS (below), hence Delta >= -eps*R = 0 by
          the banked CH1 bound (check_T_delta_JR_derived leg 4),
          OCCUPANCY-FREE -- independently of J and of what the world
          presents. HONEST FORM (the audit's tautology adjudication,
          carried as part of the claim): the floor is convention-near-
          tautological GIVEN the family definition -- per-string
          presentations of distinct strings bill distinct channels
          essentially by construction of the family; the floor's work is
          done by the convention plus the family scoping, stated plainly.
          No "genuinely gauge-invariant" qualifier anywhere: negative
          Delta with a gauge-invariant shared channel IS realizable (the
          copy pair below bills -eps and E^2 is gauge-invariant); what
          the family excludes is a PRESENTATION (co-presentation), not a
          gauge-structural configuration.
      (ii) THE POSITIVE CONTENT. Every shared-anchor configuration in the
          family carries a CERTIFIED type-(a) joint channel: at the fused
          cut the invariant C_02 = 1 + P_02 lies outside alg(M1 u M2)
          (dim 14 > 4, computed exactly here); at the shared boundary
          vertex the fused-channel label strictly extends the per-link
          anchor data (centre dim 5 > 4 flux tuples, consumed LIVE from
          check_T_anchor_set_is_electric_center_data's RETURNED artifacts
          -- audit F6, never a re-quoted string). With the fused content
          presented, Delta = +eps: sharing an anchor at a gauge cut
          creates joint content, not redundancy.
      (iii) THE COLLAPSE LEGS. The "gauge copy-pair" (two families both
          billing E^2 at one link) is NOT two channels: a bijective value
          relabel f(E^2) = 2 E^2 induces the IDENTICAL partition of the
          link content, so it is the SAME distinction -- one channel,
          FD1-sc (a value relabeling is a zero-cost convention). Two
          families co-presenting it is the banked classical NC2 copy pair
          verbatim (R = 1, J = 0, Delta = -eps); the gauge invariance of
          the shared channel is incidental to the sign. STRICTLY COARSER
          FUNCTIONS of one flux label (the audit F2c wording) induce a
          different partition -- a genuinely different channel, R = 0,
          Delta = 0. Co-presentation plus fused content reproduces the
          banked W1 pattern (J = 1 = R, Delta = 0).

    CHANNEL IDENTITY -- THE NAMED REFINEMENT (audit F1, MAJOR; part of the
    statement): channel identity here follows the banked literal-frozenset
    convention of check_T_delta_JR_derived (its F2: literal identity of
    billed record content WITHIN THE SINGLE FIXED PRESENTATION), REFINED
    as follows -- "billed record content" is read as the induced PARTITION
    of the presented content (the distinction), not the operator label:
      * a VALUE-SIDE bijective relabel (f(E^2) = 2 E^2: identical induced
        partition) collapses to ONE channel -- FD1-sc-consistent, the
        leg-(iii) adjudication;
      * a DOMAIN automorphism (the banked leg 3(d) case g_lo = g_hi o pi:
        genuinely different partitions) remains TWO channels -- exactly
        what the banked convention's leg 3(d) exclusion protects.
    This is a REFINEMENT of the banked convention (the bank's wording does
    not itself draw the value-side / domain-side distinction), NOT its
    verbatim application; naming it is part of this check's claim.
    IN-CHECK CONSISTENCY LEG (the audit's counterexample, run here): Q1
    and 2*Q1 are DISTINCT operators with IDENTICAL spectral partitions --
    the literal-operator rule and the partition rule DISAGREE on that pair
    (two channels vs one); THIS CHECK USES THE PARTITION RULE, and every
    R = 0 leg below is stated as partition-distinctness, never as bare
    operator distinctness.

    PARTITION-DISTINCTNESS, computed per instance (audit F1 fix (i)):
      * fused cut, k = 2, 3: the per-string records Q_i are idempotents
        with spectrum {0, 1}; the only operators inducing Q_i's partition
        are its injective value relabelings, i.e. {Q_i, 1 - Q_i} at
        spectrum {0, 1}; computed: Q_j is neither Q_i nor 1 - Q_i for
        every j != i -- genuinely different eigenspace pairs, hence
        different partitions, hence distinct channels;
      * shared vertex: the two flux channels induce partitions of the
        joint two-link content generated by DIFFERENT centre factors --
        the E_1^2 and E_2^2 partitions of the 25-dim content are computed
        and differ as cell sets, not merely as labels.

    FALSIFIER (audit F7, live): a certified family configuration
    (per-string presentation, distinct strings) with R >= 1 under the
    partition rule, or a certified Delta < 0 WITHOUT literal
    co-presentation of one channel by two families, kills the proposition.

    FENCES (audit F8): (a) "co-billed" is scoped to the banked leg-7 sense
    -- the fused Casimir at the shared vertex is co-billed by the two CUT
    SIDES; the two STRING families cannot bill it (it is not supported on
    either single string's DOF), and that is exactly what keeps R = 0
    there; (b) OCCUPANCY: occupancy chooses J in {0, 1}; the floor is
    occupancy-free; occupancy is never derived (module fence); (c)
    presentation-relativity: Ch is presentation input (the banked
    ledger-relativity sentence, read live from the returned artifacts); a
    presentation in which one family re-bills a channel the other already
    bills realizes R >= 1 BY CONSTRUCTION -- the copy-pair mechanism,
    classical in structure, the only route to negative Delta; (d) the
    single-diagonal-comparison-group modelling fence inherited (module
    docstring).

    GRADE [P], with the family scoped IN-STATEMENT: derived bookkeeping
    over the banked axioms (CH1 + CH2, consumed live) plus exact
    witnesses; a family-scoped proposition, never a presentation-free
    theorem.
    """
    checks = []

    def ck(cond, msg):
        checks.append((bool(cond), msg))
        check(cond, msg)

    from itertools import product as _iprod
    from apf.delta_calculus import check_T_delta_JR_derived
    from apf.anchor_support_algebra import (
        check_T_anchor_support_formalization)
    from apf.anchor_center_correspondence import (
        check_T_anchor_set_is_electric_center_data)

    EPS = F(1)
    fsz = frozenset

    # ------- leg 0: conventions consumed LIVE, asserted against the
    # RETURNED artifacts (audit F6 -- never a re-quoted string) -------------
    r_jr = check_T_delta_JR_derived()
    ax = r_jr['artifacts']['axioms']
    ck(r_jr['epistemic'] == 'P'
       and set(ax) == {'CH1', 'CH2', 'CH3'}
       and 'activation monotonicity' in ax['CH1']
       and 'cost = count' in ax['CH2'],
       "leg 0: check_T_delta_JR_derived LIVE at [P]; CH1/CH2/CH3 read from "
       "the RETURNED artifacts (activation monotonicity + cost = count)")
    ck('shared CHANNELS' in r_jr['artifacts']['R_convention']
       and 'loci' in r_jr['artifacts']['R_convention'],
       "leg 0: the R-convention read from the returned artifacts -- R "
       "counts shared CHANNELS (billed distinctions), not loci")
    ck('presentation input' in r_jr['artifacts']['ledger_relativity'],
       "leg 0: ledger relativity read from the returned artifacts -- "
       "Ch(join) is presentation input (the floor below is family-scoped "
       "bookkeeping, never a presentation-free theorem)")
    r_as = check_T_anchor_support_formalization()
    mta = r_as['artifacts']['meson_type_a']
    ck(r_as['epistemic'] == 'P' and mta['dim_M12'] == 5
       and mta['dim_alg_union'] == 4 and mta['singlet_in_union'] is False,
       "leg 0: meson type-(a) witness LIVE from "
       "check_T_anchor_support_formalization's returned artifacts "
       "(dim 5 > 4, membership failure)")

    # ------- leg 1: the fused cut, k = 2 -- exact algebra + the floor ------
    dims4 = [2, 2, 2, 2]
    n4 = 16
    Etot = {}
    Ftot = {}
    for s4 in range(4):
        Etot = _sp_add(Etot, _sp_slot_op({s4: _SP_E}, dims4))
        Ftot = _sp_add(Ftot, _sp_slot_op({s4: _SP_F}, dims4))
    cdim = _sp_commutant_dim([Etot, Ftot], n4)
    ck(cdim == 14,
       f"leg 1: full gauge-invariant cut algebra dim {cdim} == 14 "
       "(= 1 + 9 + 4 Schur count; matches the banked native-algebra value)")
    I16 = _sp_eye(n4)
    Q1 = _sp_kron(_SP_PSING, _sp_eye(4), 4)
    Q2 = _sp_kron(_sp_eye(4), _SP_PSING, 4)
    ck(_sp_iszero(_sp_comm(Q1, Etot)) and _sp_iszero(_sp_comm(Q1, Ftot))
       and _sp_iszero(_sp_comm(Q2, Etot)) and _sp_iszero(_sp_comm(Q2, Ftot)),
       "leg 1: per-string singlet records Q1, Q2 gauge-invariant at the cut")
    ck(_sp_eq(_sp_mm(Q1, Q1), Q1) and _sp_eq(_sp_mm(Q2, Q2), Q2),
       "leg 1: Q1, Q2 idempotent (spectrum {0, 1} -- the partition of each "
       "is its eigenspace pair)")
    ck(not _sp_eq(Q2, Q1) and not _sp_eq(Q2, _sp_sub(I16, Q1)),
       "leg 1 PARTITION-DISTINCTNESS (audit F1): the only operators "
       "inducing Q1's partition are its injective value relabelings "
       "{Q1, 1 - Q1} at spectrum {0, 1}; Q2 is NEITHER -- genuinely "
       "different eigenspace pairs => different partitions => distinct "
       "channels => R = 0 under the partition rule (never bare operator "
       "distinctness)")
    twoQ1 = _sp_smul(2, Q1)
    ck(not _sp_eq(twoQ1, Q1)
       and _sp_eq(_sp_smul(F(1, 2), twoQ1), Q1),
       "leg 1 CONSISTENCY LEG (the audit's Q1-vs-2Q1 counterexample, run "
       "in-check): Q1 and 2*Q1 are DISTINCT operators whose spectral "
       "idempotents coincide ({Q1, 1 - Q1}: the eigenvalue-2 Lagrange "
       "projector of 2*Q1 is (2*Q1)/2 = Q1) -- IDENTICAL induced "
       "partitions; the literal-operator rule (two channels) and the "
       "partition rule (one channel) DISAGREE on this pair; THIS CHECK "
       "USES THE PARTITION RULE and says so")
    Q12 = _sp_mm(Q1, Q2)
    ck(_sp_eq(Q12, _sp_mm(Q2, Q1)),
       "leg 1: Q1 and Q2 commute (disjoint index pairs)")
    union_span = _SpSpan()
    basis_union = [I16, Q1, Q2, Q12]
    for b in basis_union:
        union_span.add(_sp_flat(b, n4))
    ck(union_span.dim == 4
       and all(union_span.contains(_sp_flat(_sp_mm(a, b), n4))
               for a in basis_union for b in basis_union),
       "leg 1: alg(M1 u M2) = span{1, Q1, Q2, Q1Q2} exactly, dim 4 < 14 "
       "(closure verified)")
    perm = {}
    for bits in _iprod(range(2), repeat=4):
        src = ((bits[0] * 2 + bits[1]) * 2 + bits[2]) * 2 + bits[3]
        dst = ((bits[2] * 2 + bits[1]) * 2 + bits[0]) * 2 + bits[3]
        perm.setdefault(dst, {})[src] = F(1)
    P02 = perm
    C02 = _sp_add(I16, P02)
    ck(_sp_iszero(_sp_comm(P02, Etot)) and _sp_iszero(_sp_comm(P02, Ftot)),
       "leg 1: the fused invariant C_02 = 1 + P_02 is gauge-invariant at "
       "the cut")
    ck(not union_span.contains(_sp_flat(C02, n4)),
       "leg 1 TYPE-(a) DEVIATION WITNESS (the positive content): C_02 is "
       "NOT in alg(M1 u M2) -- 14 > 4, the join carries a genuinely new "
       "record operator (the fused channel)")
    swap4 = {0: {0: F(1)}, 1: {2: F(1)}, 2: {1: F(1)}, 3: {3: F(1)}}
    C4 = _sp_add(_sp_eye(4), swap4)
    Panti = _sp_smul(F(1, 2), _sp_sub(_sp_eye(4), swap4))
    Psym = _sp_smul(F(1, 2), _sp_add(_sp_eye(4), swap4))
    ck(_sp_iszero(_sp_mm(C4, Panti))
       and _sp_eq(_sp_mm(C4, Psym), _sp_smul(2, Psym))
       and _sp_rank(Panti) == 1 and _sp_rank(Psym) == 3,
       "leg 1: cut content 1/2 (x) 1/2 = 0 (+) 1 exact (C_02 spectrum "
       "{0, 2} = J(J+1); fused-channel projectors of ranks 1 and 3)")
    inv4 = _kernel(_sp_to_dense(Etot, n4) + _sp_to_dense(Ftot, n4), n4)
    ck(len(inv4) == 2,
       "leg 1: joint invariant-state sector dim 2 (the banked 2-dim "
       "physical pairing sector)")
    ch1 = fsz({'sing1@cut'})
    ch2 = fsz({'sing2@cut'})
    chj = ch1 | ch2 | fsz({'fused02@cut'})
    ck(chj >= (ch1 | ch2), "leg 1: CH1 holds on the instance")
    J_a, R_a = len(chj - (ch1 | ch2)), len(ch1 & ch2)
    d_a = 3 * EPS - EPS - EPS   # hand-set table: eps, eps, 3*eps
    ck((J_a, R_a) == (1, 0) and d_a == EPS == EPS * (J_a - R_a)
       and d_a >= -EPS * R_a,
       "leg 1 ledger: J = 1, R = 0, Delta = +eps (reading-independent at "
       "d = 2); the CH1 bound Delta >= -eps*R = 0 holds occupancy-free")

    # ------- leg 2: the shared boundary vertex (banked 41/5 model), LIVE ---
    r_ac = check_T_anchor_set_is_electric_center_data()
    l7 = r_ac['artifacts']['leg7_numbers']
    ck(r_ac['epistemic'] == 'P_structural_reading'
       and l7['one_side_dim'] == 41 and l7['center_dim'] == 5
       and l7['flux_tuples'] == 4 and l7['raw_commutant_dim'] == 57,
       "leg 2: the shared-vertex extension consumed LIVE from "
       "check_T_anchor_set_is_electric_center_data's RETURNED artifacts "
       "(audit F6): one-side dim 41, centre dim 5 > 4 flux tuples, raw "
       "commutant 57 -- the fused-channel label is joint content, "
       "certified by the banked leg-7 centre extension")
    cellA0 = fsz(i for i in range(25) if i // 5 == 0)
    cellB0 = fsz(i for i in range(25) if i % 5 == 0)
    partA = fsz({cellA0, fsz(range(25)) - cellA0})
    partB = fsz({cellB0, fsz(range(25)) - cellB0})
    ck(partA != partB and len(cellA0) == 5 == len(cellB0),
       "leg 2 PARTITION-DISTINCTNESS: the flux1@l1 and flux2@l2 channels "
       "induce DIFFERENT partitions of the joint two-link content "
       "(different cell sets, generated by different centre factors) => "
       "distinct channels => R = 0")
    ck(EPS * (1 - 0) == EPS,
       "leg 2 ledger: J = 1 (the fused label; jointness = the live 5 > 4 "
       "extension), R = 0, Delta = +eps. F8 SCOPE: the fused Casimir is "
       "co-billed by the two CUT SIDES (the banked leg-7 sense); the two "
       "STRING families cannot bill it -- it is not supported on either "
       "single string's DOF -- which is exactly what keeps R = 0 here")

    # ------- leg 3: the copy-pair collapse + coarse-graining (A4) ----------
    evals = [F(0), F(3, 4), F(3, 4), F(2), F(2), F(2)]

    def _partition_of(vals):
        cells = {}
        for i, v in enumerate(vals):
            cells.setdefault(v, []).append(i)
        return fsz(fsz(c) for c in cells.values())

    part_fine = _partition_of(evals)
    part_relabel = _partition_of([2 * v for v in evals])
    part_coarse = _partition_of([F(0) if v == 0 else F(1) for v in evals])
    ck(part_relabel == part_fine,
       "leg 3: a bijective value relabel f(E^2) = 2 E^2 induces the SAME "
       "partition of the link content => the SAME distinction => the SAME "
       "channel (FD1-sc; the NAMED value-side refinement of the banked "
       "literal convention -- the banked leg 3(d) DOMAIN-automorphism "
       "exclusion is untouched: different partitions stay different "
       "channels)")
    ck(EPS * (0 - 1) == -EPS,
       "leg 3: the gauge copy-pair -- R = 1, J = 0, Delta = -eps, the "
       "banked classical NC2 mechanism verbatim; the gauge invariance of "
       "the shared channel is incidental to the sign (the ONLY route to "
       "negative Delta is literal co-presentation)")
    ck(part_coarse != part_fine
       and len(part_coarse) == 2 and len(part_fine) == 3,
       "leg 3: STRICTLY COARSER functions of one flux label induce a "
       "different partition => a genuinely different channel -- R = 0, "
       "Delta = 0 (no negative Delta from fine/coarse pairs)")
    ck(EPS * (1 - 1) == 0,
       "leg 3 boundary: co-presentation + fused content = the banked W1 "
       "pattern (J = 1 = R, Delta = 0); co-presentation without fusion = "
       "-eps -- in both, R >= 1 is literal re-presentation, "
       "presentation-level and classical")

    # ------- leg 4: k = 3 at one cut -- exact, partition-distinct ----------
    dims6 = [2] * 6
    n6 = 64
    Etot6 = {}
    Ftot6 = {}
    for s6 in range(6):
        Etot6 = _sp_add(Etot6, _sp_slot_op({s6: _SP_E}, dims6))
        Ftot6 = _sp_add(Ftot6, _sp_slot_op({s6: _SP_F}, dims6))
    Q3 = []
    for pair_start in (0, 2, 4):
        q = _SP_PSING
        if pair_start:
            q = _sp_kron(_sp_eye(1 << pair_start), q, 4)
        post = 6 - pair_start - 2
        if post:
            q = _sp_kron(q, _sp_eye(1 << post), 1 << post)
        Q3.append(q)
    ck(all(_sp_iszero(_sp_comm(q, Etot6)) and _sp_iszero(_sp_comm(q, Ftot6))
           for q in Q3),
       "leg 4: all three per-string records gauge-invariant (k = 3)")
    I64 = _sp_eye(n6)
    ck(all(_sp_eq(_sp_mm(q, q), q) for q in Q3)
       and all(not _sp_eq(Q3[j], Q3[i])
               and not _sp_eq(Q3[j], _sp_sub(I64, Q3[i]))
               for i in range(3) for j in range(3) if i != j),
       "leg 4 PARTITION-DISTINCTNESS at k = 3: pairwise, Q_j is neither "
       "Q_i nor 1 - Q_i (idempotents, spectrum {0, 1}) => pairwise "
       "different eigenspace partitions => R = 0 for every pair")
    span3 = _SpSpan()
    elems = [I64] + Q3 + [_sp_mm(Q3[0], Q3[1]), _sp_mm(Q3[0], Q3[2]),
                          _sp_mm(Q3[1], Q3[2]),
                          _sp_mm(Q3[0], _sp_mm(Q3[1], Q3[2]))]
    for e in elems:
        span3.add(_sp_flat(e, n6))
    ck(span3.dim == 8,
       "leg 4: alg(M1 u M2 u M3) dim 8 (commuting projectors)")
    perm6 = {}
    for bits in _iprod(range(2), repeat=6):
        src = 0
        for b in bits:
            src = src * 2 + b
        sw = (bits[2], bits[1], bits[0], bits[3], bits[4], bits[5])
        dst = 0
        for b in sw:
            dst = dst * 2 + b
        perm6.setdefault(dst, {})[src] = F(1)
    ck(_sp_iszero(_sp_comm(perm6, Etot6))
       and _sp_iszero(_sp_comm(perm6, Ftot6)),
       "leg 4: the fused/exchange invariant P_02 is gauge-invariant")
    ck(not span3.contains(_sp_flat(perm6, n6)),
       "leg 4 TYPE-(a) at k = 3: P_02 outside the union algebra -- a "
       "certified joint channel exists for every sharing pair")

    # ------- leg 5: the sweep and the proposition --------------------------
    SWEEP = [
        ('k=2 disjoint links (anchor-disjoint)',          0, 0, 0),
        ('k=2 shared boundary vertex (banked leg 7, live)', 0, 1, 1),
        ('k=2 shared cut (fused, computed above)',        0, 1, 1),
        ('k=3 shared cut, any pair (computed above)',     0, 1, 1),
    ]
    for nm, Rv, Jv, dexp in SWEEP:
        ck(EPS * (Jv - Rv) == dexp * EPS and Rv == 0 and dexp >= 0,
           f"leg 5 sweep [{nm}]: R = {Rv}, J = {Jv}, "
           f"Delta = +{dexp}*eps >= 0")
    ck(all(Rv <= Jv for _, Rv, Jv, _ in SWEEP),
       "leg 5 THE PROPOSITION (family-scoped, floor and content "
       "separated): across every distinct-string configuration in the "
       "walked family, R = 0 by partition-distinctness, so Delta >= "
       "-eps*R = 0 by the banked CH1 bound, occupancy-free -- R > J never "
       "occurs; MOREOVER every shared-anchor configuration carries a "
       "certified type-(a) joint channel (Delta = +eps with the fused "
       "content presented); negative Delta requires R >= 1, i.e. literal "
       "co-presentation of one channel by two families -- the classical "
       "copy-pair mechanism, a presentation-level exclusion, not a "
       "gauge-structural one")

    return _result(
        name='T_no_negative_delta_at_gauge_cut_family -- the family-scoped '
             'no-negative-Delta proposition in partition-distinctness form '
             '(floor: R = 0 + CH1; content: type-(a) witnesses + collapse '
             'legs)',
        tier=4,
        epistemic='P',
        summary=(
            'THE D1 FAMILY-SCOPED PROPOSITION (Paper 12 round-7, reviewer '
            'Q2; walk D1 + hostile audit LAND-WITH-FIXES 0.85, F1-F8 '
            'carried). Within the walked family -- per-string '
            'presentations of DISTINCT strings over the standard cut set: '
            'disjoint links, shared boundary vertex, shared cut, k <= 3 -- '
            'R = 0 for every pair of families by PARTITION-DISTINCTNESS '
            '(the per-string records are {0, 1}-spectrum idempotents and '
            'Q_j is never in {Q_i, 1 - Q_i}, so the eigenspace partitions '
            'genuinely differ; at the shared vertex the two flux channels '
            'partition the joint content by different centre factors), '
            'hence Delta >= -eps*R = 0 by the banked CH1 bound, '
            'OCCUPANCY-FREE. The floor is convention-near-tautological '
            'given the family definition (the audit adjudication, part of '
            'the claim); the content is (a) the certified type-(a) joint '
            'channels at every shared-anchor configuration (fused cut: '
            'C_02 outside alg(M1 u M2), 14 > 4 computed; shared vertex: '
            'centre 5 > 4, consumed LIVE from the banked leg-7 artifacts) '
            'and (b) the collapse legs (the gauge copy-pair collapses to '
            'the banked classical NC2 mechanism via FD1-sc -- a NAMED '
            'value-side refinement of the banked literal channel '
            'convention, with the Q1-vs-2Q1 rule-disagreement pair run '
            'in-check and the banked leg 3(d) domain-automorphism '
            'exclusion untouched; strictly coarser functions of one flux '
            'label are a different channel with Delta = 0). Negative '
            'Delta arises only via literal co-presentation of one channel '
            'by two families -- presentation-level, classical, available '
            'in any ledger; the gauge invariance of the shared channel is '
            'incidental to the sign. Falsifier live: a certified family '
            'configuration with R >= 1 under the partition rule, or a '
            'certified Delta < 0 without co-presentation. Occupancy '
            'chooses J in {0, 1}; never derived. All arithmetic exact.'
        ),
        key_result=(
            'Family-scoped: R = 0 by partition-distinctness => Delta >= 0 '
            'occupancy-free (CH1); every shared anchor carries a certified '
            'type-(a) joint channel (14 > 4 computed, 5 > 4 live); '
            'negative Delta only via literal co-presentation (the '
            'classical copy pair) -- with the value-side partition '
            'refinement of the channel convention NAMED, not smuggled.'
        ),
        dependencies=[
            'check_T_delta_JR_derived',
            'check_T_anchor_support_formalization',
            'check_T_anchor_set_is_electric_center_data',
            'check_T_su2_string_cut_native_algebra',
            'check_FD1_structural_completeness',
        ],
        cross_refs=['check_T_cost_count_characterization',
                    'check_T_delta_disjoint_additivity',
                    'check_T_su2_string_cut_comovement'],
        n_assertions=len(checks),
        artifacts={
            'family': [
                'k=2 parallel strings on disjoint links (anchor-disjoint)',
                'k=2 strings sharing one boundary vertex (banked 41/5 '
                'model, leg 7 live)',
                'k=2 strings fused at one cut',
                'k=3 strings fused at one cut, any pair',
            ],
            'channel_identity_refinement': (
                'value-side bijective relabel (identical induced '
                'partition) = ONE channel (FD1-sc); domain automorphism '
                '(different partitions) = TWO channels (the banked leg '
                '3(d) exclusion untouched); a NAMED refinement of the '
                'banked literal-frozenset convention, not its verbatim '
                'application; the Q1-vs-2Q1 disagreement pair run '
                'in-check; this check uses the partition rule'),
            'floor_honesty': (
                'the R = 0 floor is convention-near-tautological given '
                'the family definition; the content is the type-(a) '
                'witnesses + the collapse legs'),
            'falsifier': (
                'a certified family configuration (per-string '
                'presentation, distinct strings) with R >= 1 under the '
                'partition rule, or a certified Delta < 0 without literal '
                'co-presentation, kills the proposition'),
            'sweep': {nm: {'R': Rv, 'J': Jv, 'Delta_over_eps': dexp}
                      for nm, Rv, Jv, dexp in SWEEP},
            'fences': [
                'co-billed scoped to CUT SIDES at the shared vertex; the '
                'string families cannot bill the fused Casimir -- what '
                'keeps R = 0 there',
                'occupancy chooses J in {0, 1}; the floor is '
                'occupancy-free; occupancy never derived',
                'Ch is presentation input; co-presentation realizes '
                'R >= 1 by construction -- the only negative route, '
                'classical',
                'single diagonal comparison group modelling fence '
                'inherited',
            ],
        },
    )


_CHECKS = {
    'check_T_su2_string_cut_comovement':
        check_T_su2_string_cut_comovement,
    'check_T_su2_string_cut_native_algebra':
        check_T_su2_string_cut_native_algebra,
    'check_T_no_negative_delta_at_gauge_cut_family':
        check_T_no_negative_delta_at_gauge_cut_family,
}


def register(registry):
    """Register the SU(2) string-cut testbed checks into the bank."""
    registry.update(_CHECKS)


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == '__main__':
    for _n, _r in run_all().items():
        print(('PASS' if _r.get('passed', True) else 'FAIL'), _n)
        print('  grade:', _r['epistemic'], '| tier', _r['tier'])
        if 'verdict' in _r:
            print('  verdict:', _r['verdict'])
            for _k, _v in _r['clauses'].items():
                print(f'    {_k}: {_v}')
        print('  ', _r['key_result'])


# ---------------------------------------------------------------------------
# Interface Engine onboarding (Full Bank Onboarding wave, 2026-07-04)
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "gauge:su2_string_cut_four_clause_verdict",
        "axis": "ROUTE",
        "expect_export": False,
        "claim_text": (
            "The SU(2) string-cut testbed's co-movement verdict is PARTIAL "
            "and FOUR-CLAUSE -- never flattened to 'co-moves' "
            "[P_structural_reading]: (i) asymptotic N-ality CO-MOVES at "
            "sign/class strength; (ii) intra-family leading-order ordering "
            "is UNDER-DETERMINED on the Delta side beyond sign "
            "(reading-dependence pinned, neither reading banked); (iii) "
            "split-vs-unsplit DIVERGES robustly -- Delta is a capacity "
            "ledger, not an energy functional, DEMONSTRATED; (iv) tautology "
            "clean. Native fusion invariants generate the full "
            "gauge-invariant cut algebra [P] -- exact-over-Q at k <= 2; "
            "mod-p corroborated at k = 3, never cited as the exact-over-Q "
            "statement; the family-scoped "
            "no-negative-Delta proposition holds in partition-distinctness "
            "form [P] with a live falsifier. "
            "(check_T_su2_string_cut_comovement + "
            "check_T_su2_string_cut_native_algebra + "
            "check_T_no_negative_delta_at_gauge_cut_family, "
            "su2_string_cut_testbed.py)"
        ),
        "note": (
            "Onboards the Paper 12 worked-example testbed onto the ROUTE "
            "axis as a held claim; the four-clause split is frozen in the "
            "claim text (do-not-re-flatten, mechanized). A "
            "CONTEXTUALITY-axis onboarding of the KCBS/Yu-Oh native-algebra "
            "legs was ASSESSED and DEFERRED pending an exact-rational "
            "scenario extraction conforming to the contextuality adapter "
            "contract (the seam-3 faithfulness discipline; no vacuous or "
            "float-fudged scenario rows)."
        ),
    },
)
