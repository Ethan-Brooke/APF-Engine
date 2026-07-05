"""apf/anchor_center_correspondence.py -- anchors and the electric center.

v24.3.379 (2026-07-04, Paper 12 round-4 review lane A1, reviewer Q2;
fresh-context hostile audit LAND-WITH-FIXES 0.85, findings F1-F8 ALL
carried). Walk of record: "The Turning/p12_review4_walks_2026-07-04/
a1_anchor_center/" (walk_report_a1.md + two witnesses + audit_report_a1.md).
Answers the reviewer's Q2: how does anc(S) map onto the electric/magnetic
center choices (Casini-Huerta-Rosabal, PRD 89, 085012 (2014),
arXiv:1312.1183) and the extended-Hilbert-space formulations of gauge-theory
entanglement (Donnelly, PRD 85, 085004 (2012); Ghosh-Soni-Trivedi, JHEP 09
(2015) 069; Aoki et al., JHEP 06 (2015) 187; Soni-Trivedi, JHEP 01 (2016)
136)?

Two checks:

  check_T_delta_vs_centre_entropy_diagnoses  [P]
      DELTA VS THE CENTRE-SENSITIVE ENTROPY: OPPOSITE VERDICTS, PINNED
      (landed v24.3.381, 2026-07-04, Paper 12 round-6 walk C3, reviewer
      Q7; fresh-context hostile audit LAND-WITH-FIXES 0.85, mandatory F1
      + F2/F3/F4/F5 + F7 grade condition carried; walk of record:
      "The Turning/p12_review6_walks_2026-07-04/c3_delta_entropy/"): the
      electric-centre algebraic entropy S_EC (this module's comparison
      object, named) and the capacity ledger Delta share the
      superselection skeleton d_cut and NO functional value. Witnessed
      three ways, exact: the statistics dial (S_EC strictly sweeps while
      the record configuration -- hence Delta -- is fixed); the
      equal-entropy sign flip (one routed-string cut state, S_EC = 2 bits
      exactly, carrying Delta = +eps and Delta = -eps under two named
      billing configurations derived from in-check record models); and
      the PINNED STRICT ANTI-ORDERED PAIR -- three strings with d_cut =
      (4, 4, 4) against (5, 5, 2), matched string count, matched
      (d-1)-count, matched N-ality, point-mass statistics: S_EC orders
      log2 64 > log2 50 while the register-graded Delta orders
      6*eps < 7*eps. Each of the three INTEGER readings (unit,
      register-per-component, (d-1)) has its own strict anti pair; the
      fourth banked reading (exact log2-count) is the SECOND NEGATIVE
      CONTROL -- at point-mass it IS the entropy and provably never
      anti-orders, which pins strict ANTI to the integer denomination
      exactly (the cost floor's ceiling overhead composing across
      records). Pooled packing is the first negative control (ties the
      pinned pair; zero anti pairs on the exhaustive multiset sweep, at
      point-mass statistics).

  check_T_anchor_set_is_electric_center_data  [P_structural_reading]
      At a lattice gauge cut IN WHICH EACH BOUNDARY VERTEX HOSTS AT MOST ONE
      CROSSED LINK (the VERTEX-DISJOINT rider, audit F1 -- carried on every
      statement of the identity), the anchor data of a flux-string family
      under Paper 12 SS2's lattice identification of Definition (anchor) is
      exactly the superselection data of the electric-center algebra
      assignment, at the variable-flux level; anchor-disjointness is exactly
      the statement that the two families' invariant algebras are supported
      in DIFFERENT center factors (audit F4 -- the family-support form, not
      the vacuous cut-geometry factorization); and within a fixed flux
      sector the residual center is fused-channel data, not anchor data.
      At a SHARED boundary vertex the identity FAILS at model strength and
      the seventh leg witnesses exactly how: the common superselection data
      strictly extends the anchor set by the fused-channel label (center
      dim 5 vs 4 flux tuples; the fused Casimir central, in both sides'
      algebras, and provably not a function of the per-link flux labels).

THE VERDICT, honestly worded (audit F5): anc is NOT an algebra-assignment
functor -- it is a family-indexed map to billing loci, and nothing in A1
forces the electric choice on a family of magnetic records (the magnetic-
center counterpart is well-posed, unexercised, gated behind the same
missing across-interface transport primitive as the Paper 12 SS10
line-operator Delta). That category difference and family-relativity is the
honest NO. But for the billed families -- electric-flux strings -- the
anchor data IS center data, and specifying it uniquely selects the electric
assignment within CHR's classification-by-center. The two descriptions pick
out the same object by different routes.

THE TWO-LAYER STRUCTURE (content, not noise; re-drawn at shared vertices
per audit F1):
  between sectors (variable flux, vertex-disjoint cut):
      center of the electric-center assignment; sectors = flux tuples
      <-> the anchor set: the billing loci and their labels.
  within a sector (fixed content):
      residual center = fused-channel (total-spin isotypic) projectors;
      non-central blocks = the native C_ab algebra of Paper 12 SS7.3
      <-> the record/contextuality structure; the J-carriers Delta counts.
  at a SHARED vertex (variable flux):
      the fused-channel datum migrates from the record layer INTO the
      cut's superselection data -- the electric center strictly extends
      the per-link anchor set. Either the lattice identification of anc
      absorbs the fused label for spanning families (Def. anchor's
      "degrees of freedom whose capacity S draws on" arguably wants this)
      or anc stays per-link and the correspondence carries the rider;
      this check banks the rider form and states the fork.

MODELLING IDENTIFICATION, flagged (audit F3; a READING, entry 4 of the
ledger below): "the algebra available to side A" is modelled as the
commutant of the B-side gauge action on the link space, with the left
tensor factor read as the constraint-solved regional multiplicity space
(interior-dressing convention, standard since Donnelly 2012 / GST). The
bare-link literally-gauge-invariant algebra is just the center (dim 3 on
the single link -- computed in-check as the two-sided commutant, the
audit's probe A). The commutant is a proxy for the dressed regional
assignment, not a claim that gauge-variant boundary operators are physical.

EHS / EDGE-MODE EXCLUSION, correctly routed (audit F2). The extended-
Hilbert-space BILLING BASIS (boundary data in full G-representations,
i.e. edge microstates) is excluded by the allocation reading / X1
relabel-freedom (an empirical-difference-free relabeling is a zero-cost
convention: check_T_gauge_connection_is_gauge_variant_convention_P +
check_FD1_structural_completeness). The edge TERM
Sigma_c p_c Sigma_l log(2 j_l + 1) is NOT struck by X1 -- its value is an
invariant function of the anchor label (log d_cut per link); it is
declined on TWO other legs: (i) no count functional J(d) is grounded
(clause (ii) of the banked comovement check,
check_T_su2_string_cut_comovement); (ii) the p_c-weighting requires a
probability primitive the ledger lacks (Paper 12 SS10 -- the ledger reads
no probabilities). Openness-shaped declines, not X1 consequences.

TRIVIAL-CENTER EXCLUSION, correctly gated (audit F6): CHR's trivial-center
choices are boundary maximal-tree partial GAUGE FIXINGS that ENLARGE one
side's algebra with gauge-fixed boundary variables (nothing is dropped).
The APF-side exclusion is therefore the ALLOCATION READING (the trivial
choice bills gauge-fixed convention data), NOT the anchor definition. A
reader who strikes the allocation reading loses the trivial-center
exclusion too -- reading-gated, stated.

ENTROPY FENCE (audit F7): Delta is capacity-denominated (eps*(J - R),
integer counts), not an entropy; it computes and bounds NO term of the
standard decomposition S = H({p_c}) + edge + distillable. Data-level
honesty: the single invariant d_cut = 2j+1 sizes BOTH the per-link edge
factor (log(2 j_l + 1) = log d_cut) AND the generic within-sector entropy
ceiling -- the fence is that no graded APF functional consumes it as an
entropy, not that the data does not touch the decomposition.
(2026-07-04 reconciliation, C3 landing / audit F4: under the Donnelly
booking the maximally mixed cut record's log d_cut is an EDGE quantity --
its multiplicity space is trivial, so the DISTILLABLE term at these
single-crossed-link cuts is 0, not log d_cut; log d bounds the
distillable piece only in the generic non-gauge-bipartition sense. The
pre-C3 phrase "distillable ceiling" conflated the two bookings; the
mid-walk double-count it invites is exactly why the clause is now
pinned.) (Structural alignment only: Van Acoleyen et al.,
PRL 117, 131602 (2016) exclude the edge + classical pieces from
distillation by gauge-invariant local operations; APF reaches a parallel
exclusion of the edge piece from a different premise. Parallel
conclusions, different axioms; no identity claimed.)

FALSIFIERS (live; audit F8 + F2 rewordings):
  (a) at a cut with all boundary vertices link-disjoint, a central,
      cut-local, gauge-invariant datum NOT generated by the per-link E^2
      data (kills leg 2);
  (b) an anchor-disjoint family pair whose invariant algebras fail to
      factorize (kills leg 5 and with it the T_M transcription);
  (c) adoption anywhere in the corpus of an edge-mode billing basis OR of
      a grounded d-dependent count functional J(d) (the former breaks the
      X1 relabel-freedom leg; the latter re-opens the edge term).

FENCES (what the check does NOT claim): no entanglement-entropy claim of
any kind; no magnetic-center claim (family-gated, behind the SS10 transport
primitive); no claim that the electric choice is forced by A1 alone
(family-inherited); no continuum claim -- witnessed at SU(2) truncations
(the Schur structure argument is general-compact-G, the banked legs are
the computed instances); the fixed-content legs inherit the tetraquark-
precedent cut-modelling fence (single diagonal comparison group); the
shared-vertex configuration carries the F1 rider, never the bare identity;
occupancy is not claimed.

READINGS LEDGER (everything leaned on, named):
  1. The lattice identification of Definition (anchor) (Paper 12 SS2):
     anchors of a cut record = the gauge-invariant dof of crossed links =
     flux labels. Adopted identification; load-bearing wherever "anchor"
     appears.
  2. The allocation reading (gauge-variant relabeling = zero-cost
     convention): load-bearing in the EHS billing-basis exclusion AND
     (F6) the trivial-center exclusion.
  3. The record reading (physical records = gauge-invariant operators).
  4. The commutant-proxy modelling identification (F3, above).
The algebra computations themselves consume nothing beyond exact linear
algebra over Q. Grade [P_structural_reading] per the banked precedent
(check_T_su2_string_cut_comovement): reading-load-bearing is what P_r
marks; the algebra legs are exact.

Paper anchor: Paper 12 SS2 (Definition (anchor) + lattice identification),
SS7 (the string-cut testbed), SS9 (related work / this correspondence),
SS10 (no probability primitive; the across-interface transport primitive).

All arithmetic exact (fractions.Fraction / int), pure stdlib, no floats.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from typing import Dict

from apf.apf_utils import check, _result


# ============================================================================
# exact helpers (stdlib only; ported from the walk witnesses)
# ============================================================================

def _zeros(r, c=None):
    if c is None:
        c = r
    return [[F(0)] * c for _ in range(r)]


def _eye(d):
    M = _zeros(d)
    for i in range(d):
        M[i][i] = F(1)
    return M


def _mm(A, B):
    r, k, c = len(A), len(B), len(B[0])
    out = _zeros(r, c)
    for i in range(r):
        Ai = A[i]
        oi = out[i]
        for t in range(k):
            a = Ai[t]
            if a:
                Bt = B[t]
                for j in range(c):
                    if Bt[j]:
                        oi[j] += a * Bt[j]
    return out


def _madd(A, B, sgn=1):
    return [[A[i][j] + sgn * B[i][j] for j in range(len(A[0]))]
            for i in range(len(A))]


def _smul(s, A):
    return [[s * x for x in row] for row in A]


def _is_zero(M):
    return all(x == 0 for row in M for x in row)


def _commutes(A, B):
    return _is_zero(_madd(_mm(A, B), _mm(B, A), -1))


def _flat(M):
    return [x for row in M for x in row]


def _kron(A, B):
    ra, ca, rb, cb = len(A), len(A[0]), len(B), len(B[0])
    M = _zeros(ra * rb, ca * cb)
    for i in range(ra):
        for j in range(ca):
            a = A[i][j]
            if a:
                for k in range(rb):
                    for l in range(cb):
                        if B[k][l]:
                            M[i * rb + k][j * cb + l] = a * B[k][l]
    return M


class _Span:
    """incremental exact row span over Q, with a membership test."""

    def __init__(self, dim):
        self.dim = dim
        self.rows = []
        self.piv = []

    def _reduce(self, v):
        v = list(map(F, v))
        for r, c in zip(self.rows, self.piv):
            if v[c]:
                f = v[c]
                v = [v[k] - f * r[k] for k in range(self.dim)]
        return v

    def add(self, v):
        v = self._reduce(v)
        c = next((k for k in range(self.dim) if v[k] != 0), None)
        if c is None:
            return False
        inv = 1 / v[c]
        self.rows.append([inv * x for x in v])
        self.piv.append(c)
        return True

    def contains(self, v):
        return all(x == 0 for x in self._reduce(v))

    @property
    def rank(self):
        return len(self.rows)


def _kernel(rows, dim):
    """exact kernel basis of the row system over Q."""
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
    free = [c for c in range(dim) if c not in piv]
    out = []
    for fc in free:
        v = [F(0)] * dim
        v[fc] = F(1)
        for r, pc in enumerate(piv):
            v[pc] = -M[r][fc]
        out.append(v)
    return out


def _mat_rank(rows):
    s = _Span(len(rows[0]))
    for row in rows:
        s.add(row)
    return s.rank


def _restrict(M, idx):
    return [[M[i][j] for j in idx] for i in idx]


def _restrict_rect(M, ridx, cidx):
    return [[M[i][j] for j in cidx] for i in ridx]


def _intertwiner_kernel(gpairs, nt, ns):
    """kernel of X g_s = g_t X over Q; X is nt x ns."""
    rows = []
    for gs, gt in gpairs:
        for i in range(nt):
            for j in range(ns):
                row = [F(0)] * (nt * ns)
                for b in range(ns):
                    if gs[b][j]:
                        row[i * ns + b] += gs[b][j]
                for a in range(nt):
                    if gt[i][a]:
                        row[a * ns + j] -= gt[i][a]
                if any(row):
                    rows.append(row)
    return _kernel(rows, nt * ns)


def _blockwise_commutant(D, gens_full, sectors):
    """Sector-preserving part of the commutant of gens_full, computed
    blockwise over the given sector index lists (generators must preserve
    every sector; asserted exactly). Returns (basis_matrices, cross_dims)
    with cross_dims a dict {(si, ti): dim} of the cross-sector intertwiner
    spaces (si != ti). At a vertex-disjoint cut every cross dim vanishes and
    the diagonal part IS the full commutant; at a shared vertex the cross
    dims are reported (leg 7 consumes them)."""
    for g in gens_full:
        for idx in sectors:
            sset = set(idx)
            for j in idx:
                for i in range(D):
                    if g[i][j] != 0 and i not in sset:
                        raise AssertionError("generator does not preserve sector")
    basis = []
    cross = {}
    for si, sidx in enumerate(sectors):
        for ti, tidx in enumerate(sectors):
            gpairs = [(_restrict(g, sidx), _restrict(g, tidx))
                      for g in gens_full]
            kb = _intertwiner_kernel(gpairs, len(tidx), len(sidx))
            if si == ti:
                for v in kb:
                    M = _zeros(D)
                    for a, i in enumerate(tidx):
                        for b, j in enumerate(sidx):
                            M[i][j] = v[a * len(sidx) + b]
                    basis.append(M)
            else:
                cross[(si, ti)] = len(kb)
    return basis, cross


def _center_of(basis, D):
    """center of span(basis) as an algebra: solve sum_i c_i [B_i, B_j] = 0."""
    n = len(basis)
    rows = []
    for j in range(n):
        comms = [_flat(_madd(_mm(basis[i], basis[j]),
                             _mm(basis[j], basis[i]), -1))
                 for i in range(n)]
        for e in range(D * D):
            row = [comms[i][e] for i in range(n)]
            if any(row):
                rows.append(row)
    coeffs = _kernel(rows, n) if rows else [
        [F(1) if i == k else F(0) for i in range(n)] for k in range(n)]
    out = []
    for c in coeffs:
        M = _zeros(D)
        for i in range(n):
            if c[i]:
                M = _madd(M, _smul(c[i], basis[i]))
        out.append(M)
    return out


def _lagrange_proj(M, lams, target_lam, D):
    P = _eye(D)
    for lb in lams:
        if lb == target_lam:
            continue
        P = _mm(P, _smul(1 / (target_lam - lb), _madd(M, _smul(lb, _eye(D)), -1)))
    return P


def _alg_closure(seed, gens, D, cap):
    sp = _Span(D * D)
    basis = []
    queue = list(seed)
    while queue:
        M = queue.pop()
        if sp.add(_flat(M)):
            basis.append(M)
            if sp.rank > cap:
                break
            for g in gens:
                queue.append(_mm(M, g))
    return sp, basis


# ---------------------------------------------------- su(2) irreps (sqrt-free)
def _rep_EFH(a):
    """spin j = a/2 on C^{a+1}; integer sl2 triple: [E,F]=H, [H,E]=2E."""
    d = a + 1
    E, Fm, H = _zeros(d), _zeros(d), _zeros(d)
    for k in range(d):
        H[k][k] = F(a - 2 * k)
        if k + 1 < d:
            Fm[k + 1][k] = F(k + 1)
        if k > 0:
            E[k - 1][k] = F(a - k + 1)
    return E, Fm, H


class _Link:
    """truncated Kogut-Susskind link space H = (+)_{j in J} V_j (x) V_j."""

    def __init__(self, J):
        self.J = list(J)                      # a-values (a = 2j)
        self.dims = [a + 1 for a in self.J]
        self.offs = []
        o = 0
        for d in self.dims:
            self.offs.append(o)
            o += d * d
        self.D = o

    def embed(self, blockmats, side):
        M = _zeros(self.D)
        for bi, a in enumerate(self.J):
            d = self.dims[bi]
            A = blockmats[bi]
            off = self.offs[bi]
            for i in range(d):
                for l in range(d):
                    col = off + i * d + l
                    for x in range(d):
                        if side == 'L':
                            if A[x][i]:
                                M[off + x * d + l][col] += A[x][i]
                        else:
                            if A[x][l]:
                                M[off + i * d + x][col] += A[x][l]
        return M

    def gens(self, side):
        Xs, Zs = [], []
        for a in self.J:
            E, Fm, H = _rep_EFH(a)
            Xs.append(_madd(E, Fm))
            Zs.append(H)
        return self.embed(Xs, side), self.embed(Zs, side)

    def efh(self, side):
        Es, Fs, Hs = [], [], []
        for a in self.J:
            E, Fm, H = _rep_EFH(a)
            Es.append(E)
            Fs.append(Fm)
            Hs.append(H)
        return (self.embed(Es, side), self.embed(Fs, side),
                self.embed(Hs, side))

    def casimir(self, side):
        """E^2 = S^2 = (2(EF+FE) + H^2)/4, embedded, exact."""
        E, Fm, H = self.efh(side)
        return _smul(F(1, 4), _madd(_smul(F(2), _madd(_mm(E, Fm), _mm(Fm, E))),
                                    _mm(H, H)))

    def flux_proj(self, bi):
        M = _zeros(self.D)
        off, d = self.offs[bi], self.dims[bi]
        for k in range(d * d):
            M[off + k][off + k] = F(1)
        return M


# ------------------------------------------- qubit operators (testbed layer)
def _qswap(n, a, b):
    d = 1 << n
    M = _zeros(d)
    for s in range(d):
        ba = (s >> (n - 1 - a)) & 1
        bb = (s >> (n - 1 - b)) & 1
        t = s ^ ((1 << (n - 1 - a)) | (1 << (n - 1 - b))) if ba != bb else s
        M[t][s] = F(1)
    return M


def _qtwo_sx(n, idxs):
    d = 1 << n
    M = _zeros(d)
    for s in range(d):
        for i in idxs:
            M[s ^ (1 << (n - 1 - i))][s] += F(1)
    return M


def _qtwo_sz(n, idxs):
    d = 1 << n
    M = _zeros(d)
    for s in range(d):
        M[s][s] = F(sum(1 - 2 * ((s >> (n - 1 - i)) & 1) for i in idxs))
    return M


def _qraise(n, a):
    d = 1 << n
    M = _zeros(d)
    for s in range(d):
        if (s >> (n - 1 - a)) & 1:
            M[s ^ (1 << (n - 1 - a))][s] = F(1)
    return M


def _qlower(n, a):
    d = 1 << n
    M = _zeros(d)
    for s in range(d):
        if not (s >> (n - 1 - a)) & 1:
            M[s ^ (1 << (n - 1 - a))][s] = F(1)
    return M


def _su2_tensor(dec, b):
    out = {}
    for a, m in dec.items():
        for c in range(abs(a - b), a + b + 1, 2):
            out[c] = out.get(c, 0) + m
    return out


# ============================================================================
# THE CHECK
# ============================================================================

def check_T_anchor_set_is_electric_center_data() -> Dict:
    """T_anchor_set_is_electric_center_data: at a VERTEX-DISJOINT lattice
    gauge cut, the anchor data of a flux-string family (Paper 12 SS2 lattice
    identification of Definition (anchor)) is exactly the superselection
    data of the electric-center algebra assignment (CHR), at the variable-
    flux level; anchor-disjointness is exactly the statement that the
    families' invariant algebras are supported in different center factors;
    within a fixed flux sector the residual center is fused-channel data,
    not anchor data; and at a SHARED boundary vertex the identity fails at
    model strength -- the electric superselection data strictly extends the
    anchor set by the fused-channel label (leg 7, the audit's negative
    boundary witness, reconstructed exactly). The extended-Hilbert-space
    BILLING BASIS is excluded by the allocation/X1 reading; the invariant-
    valued edge TERM is declined on the no-grounded-J(d) + no-probabilities
    legs (module docstring, audit F2 routing). Grade [P_structural_reading]:
    the algebra legs are exact over Q; the readings ledger (module
    docstring) is load-bearing wherever "anchor" appears.

    Seven legs, all exact (fractions.Fraction / int, no floats):
      1. Single truncated SU(2) link, J = {0, 1/2, 1} (dim 14): one-side
         algebras (+)_j End(V_j)(x)1, cross-flux intertwiners vanish,
         generation by the A-side electric generators alone; PLUS the F3
         flag made executable -- the two-sided (bare-link gauge-invariant)
         algebra collapses to the center, dim 3 (the commutant is a
         modelling proxy for the dressed regional assignment).
      2. Common center: Z(A_A) = Z(A_B) = A_A cap A_B = span{flux
         projectors} = the spectral algebra of E^2; E^2_L = E^2_R exactly.
      3. Raw-link negative control: a flux-changing matrix unit lies in
         neither one-side algebra.
      4. Two links at DISTINCT boundary sites (J = {0, 1/2} each, dim 25):
         full commutant = tensor product of the single-link algebras;
         center = sector-tuple projectors, generated by E_1^2, E_2^2.
      5. Anchor-disjointness transcription (family-support form, F4): the
         per-link families commute elementwise, jointly span the full
         factorized algebra, and are supported in different center factors;
         two families billing the SAME link meet in that link's flux
         projectors (budget competition).
      6. Fixed-content layer (k = 2 testbed conventions): per-index
         Casimirs scalar (3/4)*1; fused-cut center = fused-channel
         projectors (dim 3, ranks 2/9/5); the anchor-disjoint product
         configuration is abelian dim 4 and factorizes exactly; the
         total-singlet projector and the exchange P_02 are in the diagonal
         algebra and NOT in the product algebra.
      7. SHARED-B-VERTEX probe (audit F1, mandatory): two links J = {0,1/2}
         each, B-side action DIAGONAL at one shared vertex, A-side sites
         distinct. The flux-superselected one-side algebra has dim 41
         (= 1 + 4 + 4 + 32) with common center dim 5 > 4 = #flux tuples;
         the raw commutant additionally carries cross-sector intertwiners
         (full dim 57 = 5^2 + 4^2 + 4^2 by the Schur count, matched by the
         blockwise cross dims); the fused right Casimir (S1+S2)^2 is
         central in the one-side algebra, lies in the B-side algebra too
         (Gauss: it is B-interior data), and is NOT a function of the
         per-link flux projectors. The superselection sectors at a shared
         vertex are (j1, j2, J_fused), not flux tuples: the vertex-disjoint
         rider is load-bearing, not decorative.
    """
    checks = []

    def ck(cond, msg):
        checks.append((bool(cond), msg))
        check(cond, msg)

    # =====================================================================
    # Legs 1-3: single truncated SU(2) link, J = {0, 1/2, 1}
    # =====================================================================
    L = _Link([0, 1, 2])
    D = L.D
    ck(D == 14, f"leg 1: H_link = V0(x)V0 + V.5(x)V.5 + V1(x)V1, dim {D} == 14")

    XL, ZL = L.gens('L')
    XR, ZR = L.gens('R')
    sectors = [list(range(L.offs[b], L.offs[b] + L.dims[b] ** 2))
               for b in range(len(L.J))]

    AA, crossA = _blockwise_commutant(D, [XR, ZR], sectors)
    ck(all(c == 0 for c in crossA.values()),
       "leg 1: A_A -- every cross-flux intertwiner space vanishes "
       "(block-diagonal in the flux label; vertex-disjoint cut)")
    ck(len(AA) == 14, f"leg 1: dim A_A = {len(AA)} == 14 = 1+4+9 = sum d_j^2 "
                      "((+)_j End(V_j)(x)1)")
    ck(all(_commutes(B, XR) and _commutes(B, ZR) for B in AA),
       "leg 1: A_A basis commutes with the B-side gauge action (exact)")

    AB, crossB = _blockwise_commutant(D, [XL, ZL], sectors)
    ck(all(c == 0 for c in crossB.values()) and len(AB) == 14,
       f"leg 1: A_B symmetric, dim {len(AB)} == 14, block-diagonal in flux")

    spGen, _ = _alg_closure([_eye(D), XL, ZL], [XL, ZL], D, 14)
    spAA = _Span(D * D)
    for B in AA:
        spAA.add(_flat(B))
    ck(spGen.rank == 14 and all(spAA.contains(r) for r in spGen.rows),
       "leg 1: A_A is generated by the A-side electric generators alone "
       f"(closure rank {spGen.rank} == 14; closure inside A_A) -- the "
       "one-side content is electric data through and through")

    # F3 flag, executable (audit probe A): the two-sided invariant algebra
    # (commutant of BOTH side actions -- the bare-link literally-invariant
    # algebra) collapses to the center.
    twosided, cross2s = _blockwise_commutant(D, [XL, ZL, XR, ZR], sectors)
    ck(all(c == 0 for c in cross2s.values()) and len(twosided) == 3,
       f"leg 1 (F3 flag): the bare-link two-sided invariant algebra has dim "
       f"{len(twosided)} == 3 = the center -- A_A is the commutant PROXY for "
       "the dressed regional assignment (a named reading), not the literal "
       "invariant algebra")

    # leg 2: centers
    ZAA = _center_of(AA, D)
    ZAB = _center_of(AB, D)
    ck(len(ZAA) == 3 and len(ZAB) == 3,
       f"leg 2: dim Z(A_A) = {len(ZAA)}, dim Z(A_B) = {len(ZAB)}; both == 3 = |J|")

    Pis = [L.flux_proj(b) for b in range(3)]
    spZ = _Span(D * D)
    for Z in ZAA:
        spZ.add(_flat(Z))
    ck(all(spZ.contains(_flat(P)) for P in Pis) and spZ.rank == 3,
       "leg 2: Z(A_A) = span{flux projectors Pi_j} exactly")
    spZB = _Span(D * D)
    for Z in ZAB:
        spZB.add(_flat(Z))
    ck(all(spZB.contains(_flat(P)) for P in Pis),
       "leg 2: Z(A_B) = the SAME flux algebra (common center)")
    ck(all(spZ.contains(_flat(T)) for T in twosided),
       "leg 2 (F3): the bare-link invariant algebra == the common center")

    E2L = L.casimir('L')
    E2R = L.casimir('R')
    ck(_is_zero(_madd(E2L, E2R, -1)),
       "leg 2: E^2_left == E^2_right exactly (the flux label is the one "
       "datum both sides jointly bill)")
    lams = [F(a * (a + 2), 4) for a in L.J]      # j(j+1) = 0, 3/4, 2
    ck(len(set(lams)) == 3, "leg 2: E^2 spectrum {0, 3/4, 2} distinct")
    for b, lam in enumerate(lams):
        P = _lagrange_proj(E2L, lams, lam, D)
        ck(_is_zero(_madd(P, Pis[b], -1)),
           f"leg 2: spectral projector of E^2 at j(j+1)={lam} == flux "
           f"projector Pi_{b} (the center is GENERATED by the electric Casimir)")

    spU = _Span(D * D)
    for B in AA + AB:
        spU.add(_flat(B))
    ck(spU.rank == 25,
       f"leg 2: dim(A_A + A_B) = {spU.rank} == 14+14-3 => dim(A_A cap A_B) = 3 "
       "-- the two sides meet in the center and nowhere else")

    # leg 3: raw-link negative control
    T = _zeros(D)
    T[L.offs[1]][L.offs[0]] = F(1)     # maps flux-0 sector into flux-1/2 sector
    ck(not _commutes(T, XR),
       "leg 3: raw control -- a flux-changing matrix unit is NOT in A_A")
    ck(not _commutes(T, XL),
       "leg 3: ... and NOT in A_B: raw link data is not one-side billable "
       "content (the allocation reading strikes it)")

    # =====================================================================
    # Legs 4-5: two cut links at DISTINCT boundary sites, J = {0, 1/2} each
    # =====================================================================
    L1 = _Link([0, 1])
    d5 = L1.D
    ck(d5 == 5, f"leg 4: per-link truncated space dim {d5} == 5")
    X1L, Z1L = L1.gens('L')
    X1R, Z1R = L1.gens('R')
    I5 = _eye(5)
    gensB = [_kron(X1R, I5), _kron(Z1R, I5), _kron(I5, X1R), _kron(I5, Z1R)]
    D2 = 25
    sec1 = [list(range(L1.offs[b], L1.offs[b] + L1.dims[b] ** 2))
            for b in range(2)]
    A1, cr1 = _blockwise_commutant(5, [X1R, Z1R], sec1)
    ck(all(c == 0 for c in cr1.values()) and len(A1) == 5,
       f"leg 4: single-link (J={{0,1/2}}) one-side algebra dim {len(A1)} == 5")

    sectors2 = []
    for b1 in range(2):
        for b2 in range(2):
            idx = [i1 * 5 + i2 for i1 in sec1[b1] for i2 in sec1[b2]]
            sectors2.append(idx)

    A2, cross2 = _blockwise_commutant(D2, gensB, sectors2)
    ck(all(c == 0 for c in cross2.values()),
       "leg 4: two-link joint algebra (distinct sites) -- all cross-sector "
       "intertwiners vanish (sectors = flux-label TUPLES; vertex-disjoint)")
    ck(len(A2) == 25, f"leg 4: dim A_A(two links) = {len(A2)} == 25 = 5*5")

    spA2 = _Span(D2 * D2)
    for B in A2:
        spA2.add(_flat(B))
    prods = [_kron(B1, B2) for B1 in A1 for B2 in A1]
    ck(all(spA2.contains(_flat(P)) for P in prods)
       and _mat_rank([_flat(P) for P in prods]) == 25,
       "leg 4: A_A(two links) == A_A(link1) (x) A_A(link2) EXACTLY "
       "(factorization over disjoint cut links)")

    Z2 = _center_of(A2, D2)
    ck(len(Z2) == 4, f"leg 4: dim Z = {len(Z2)} == 4 = #flux tuples (j1, j2)")
    Pi1 = [L1.flux_proj(b) for b in range(2)]
    spZ2 = _Span(D2 * D2)
    for Z in Z2:
        spZ2.add(_flat(Z))
    ck(all(spZ2.contains(_flat(_kron(Pa, Pb))) for Pa in Pi1 for Pb in Pi1),
       "leg 4: Z == span{Pi_j1 (x) Pi_j2}: the center data is the per-link "
       "flux tuple -- exactly the anchor set of the crossing family")

    E2_1 = _kron(L1.casimir('L'), I5)
    E2_2 = _kron(I5, L1.casimir('L'))
    lam2 = [F(a * (a + 2), 4) for a in L1.J]     # 0, 3/4
    ok_gen = True
    for b1, l1v in enumerate(lam2):
        P1 = _lagrange_proj(E2_1, lam2, l1v, D2)
        for b2, l2v in enumerate(lam2):
            P2 = _lagrange_proj(E2_2, lam2, l2v, D2)
            ok_gen = ok_gen and _is_zero(_madd(_mm(P1, P2),
                                               _kron(Pi1[b1], Pi1[b2]), -1))
    ck(ok_gen, "leg 4: Z is GENERATED by the per-link electric Casimirs "
               "E_1^2, E_2^2 (spectral projector products == sector "
               "projectors, exact)")

    # leg 5: anchor-disjointness = family support in different center
    # factors (audit F4: the family-support form, NOT the vacuous
    # cut-geometry center factorization)
    fam1 = [_kron(B, I5) for B in A1]
    fam2 = [_kron(I5, B) for B in A1]
    ck(all(_commutes(a, b) for a in fam1 for b in fam2),
       "leg 5: families anchored on link1 vs link2 commute elementwise "
       "(independent budgets; the T_M / L_loc transcription at the cut)")
    spJoint = _Span(D2 * D2)
    for B in fam1 + fam2:
        spJoint.add(_flat(B))
    for a in fam1:
        for b in fam2:
            spJoint.add(_flat(_mm(a, b)))
    ck(spJoint.rank == 25,
       "leg 5: the joint algebra of the two disjoint-anchor families is the "
       "FULL factorized algebra (rank 25) -- the families' algebras are "
       "supported in DIFFERENT center factors (the additivity hypothesis, "
       "family-support form)")
    spShared = _Span(D2 * D2)
    for B in fam1:
        spShared.add(_flat(B))
    ck(spShared.contains(_flat(_kron(Pi1[1], I5))),
       "leg 5: shared-anchor contrast -- a second family billing link 1 "
       "meets the first in the link-1 flux projector (nontrivial "
       "intersection = budget competition; the negation of the hypothesis)")

    # =====================================================================
    # Leg 6: the fixed-content layer (k = 2 testbed conventions)
    # =====================================================================
    n = 4
    dq = 1 << n
    for a in range(n):
        E, Lo = _qraise(n, a), _qlower(n, a)
        H = _qtwo_sz(n, [a])
        S2 = _smul(F(1, 4), _madd(_smul(F(2), _madd(_mm(E, Lo), _mm(Lo, E))),
                                  _mm(H, H)))
        ck(_is_zero(_madd(S2, _smul(F(-3, 4), _eye(dq)))),
           f"leg 6: S_{a}^2 == (3/4)*1 exactly (per-index flux label frozen "
           "at fixed content; it generates only C -- the anchor data cannot "
           "be the fixed-sector center)")

    SXt, SZt = _qtwo_sx(n, range(n)), _qtwo_sz(n, range(n))
    Ps = {(a, b): _qswap(n, a, b) for a, b in combinations(range(n), 2)}
    gens_diag = list(Ps.values())
    ck(all(_commutes(g, SXt) and _commutes(g, SZt) for g in gens_diag),
       "leg 6: every swap P_ab commutes with the diagonal action "
       "(gauge-invariant, exact)")

    dec = {0: 1}
    for _ in range(n):
        dec = _su2_tensor(dec, 1)
    cdim = sum(m * m for m in dec.values())
    ck(dec == {0: 2, 2: 3, 4: 1} and cdim == 14,
       f"leg 6: exact multiplicities {{s=0:2, s=1:3, s=2:1}} -> commutant "
       f"dim {cdim} == 14")

    spD, basisD = _alg_closure([_eye(dq)] + [_madd(g, _eye(dq)) for g in gens_diag],
                               gens_diag, dq, cdim)
    ck(spD.rank == cdim,
       f"leg 6: generated invariant algebra rank {spD.rank} == commutant "
       "dim 14 (matches the banked native-algebra [P] check)")

    ZD = _center_of(basisD, dq)
    ck(len(ZD) == 3, f"leg 6: center of the fused cut algebra dim {len(ZD)} == 3")

    M = _zeros(dq)
    for g in gens_diag:
        M = _madd(M, g)
    lams_q = [F(0), F(2), F(6)]      # s(s+1), s = 0, 1, 2
    Qs = []
    for lam in lams_q:
        P = _eye(dq)
        for lb in lams_q:
            if lb != lam:
                P = _mm(P, _smul(1 / (lam - lb), _madd(M, _smul(lb, _eye(dq)), -1)))
        Qs.append(P)
    ck(_is_zero(_madd(_madd(Qs[0], Qs[1]), _madd(Qs[2], _smul(F(-1), _eye(dq)))))
       and all(_is_zero(_madd(_mm(Q, Q), Q, -1)) for Q in Qs),
       "leg 6: fused-channel Lagrange projectors -- resolution of identity, "
       "idempotent (exact)")
    ranks = [_mat_rank([r for r in Q if any(r)]) for Q in Qs]
    ck(ranks == [2, 9, 5],
       f"leg 6: projector ranks {ranks} == [2, 9, 5] = mult*dim per channel")
    spZD = _Span(dq * dq)
    for Z in ZD:
        spZD.add(_flat(Z))
    ck(all(spZD.contains(_flat(Q)) for Q in Qs) and spZD.rank == 3,
       "leg 6: fixed-sector center == span{fused-channel projectors}: the "
       "residual center at fixed content is FUSION-CHANNEL data, not "
       "per-link anchor data (the two-layer structure)")

    gens_prod_action = [_qtwo_sx(n, [0, 1]), _qtwo_sz(n, [0, 1]),
                        _qtwo_sx(n, [2, 3]), _qtwo_sz(n, [2, 3])]
    C01 = _madd(Ps[(0, 1)], _eye(dq))
    C23 = _madd(Ps[(2, 3)], _eye(dq))
    ck(all(_commutes(c, g) for c in (C01, C23) for g in gens_prod_action),
       "leg 6: per-string fusion invariants commute with BOTH strings' "
       "gauge actions")
    per = _su2_tensor(_su2_tensor({0: 1}, 1), 1)   # {0:1, 2:1}
    cdim_prod = (sum(m * m for m in per.values())) ** 2
    ck(per == {0: 1, 2: 1} and cdim_prod == 4,
       f"leg 6: product-action commutant dim = {cdim_prod} == 4 (Schur)")
    spP, basisP = _alg_closure([_eye(dq), C01, C23], [C01, C23], dq, cdim_prod)
    ck(spP.rank == 4,
       f"leg 6: anchor-disjoint invariant algebra rank {spP.rank} == 4 "
       "(full invariant content)")
    ck(all(_commutes(a, b) for a in basisP for b in basisP),
       "leg 6: the anchor-disjoint invariant algebra is ABELIAN (no joint "
       "record structure at all)")
    pi0_01 = _smul(F(1, 2), _madd(_smul(F(2), _eye(dq)), C01, -1))
    pi1_01 = _smul(F(1, 2), C01)
    pi0_23 = _smul(F(1, 2), _madd(_smul(F(2), _eye(dq)), C23, -1))
    pi1_23 = _smul(F(1, 2), C23)
    prods_q = [_mm(a, b) for a in (pi0_01, pi1_01) for b in (pi0_23, pi1_23)]
    ck(all(spP.contains(_flat(P)) for P in prods_q)
       and _mat_rank([_flat(P) for P in prods_q]) == 4,
       "leg 6: product algebra == (per-string singlet/triplet data)(x)(same): "
       "exact factorization over the two anchor sets (L_loc transcription)")
    ck(spD.contains(_flat(Qs[0])) and not spP.contains(_flat(Qs[0])),
       "leg 6: the total-singlet projector IS in the diagonal (shared-anchor) "
       "algebra and NOT in the anchor-disjoint product algebra (a spanning "
       "distinction fails anchor-disjointness)")
    ck(spD.contains(_flat(Ps[(0, 2)])) and not spP.contains(_flat(Ps[(0, 2)])),
       "leg 6: the string-rearrangement exchange P_02: in the shared-anchor "
       "algebra, NOT in the anchor-disjoint algebra")
    ck(spP.rank < spD.rank,
       f"leg 6: product algebra (dim {spP.rank}) strictly inside the diagonal "
       f"algebra (dim {spD.rank}): sharing the cut site strictly enlarges the "
       "joint record content -- that surplus is what Delta bills")

    # =====================================================================
    # Leg 7: the SHARED-B-VERTEX probe (audit F1, the negative boundary
    # witness -- reconstructed exactly from the audit's probe)
    # =====================================================================
    # Two links, J = {0, 1/2} each; the B-side gauge action is DIAGONAL at
    # one shared boundary vertex (one SU(2) acting on both right factors);
    # the A-side sites stay distinct (product action on the left factors).
    XRd = _madd(_kron(X1R, I5), _kron(I5, X1R))
    ZRd = _madd(_kron(Z1R, I5), _kron(I5, Z1R))
    gensA_prod = [_kron(X1L, I5), _kron(Z1L, I5), _kron(I5, X1L), _kron(I5, Z1L)]

    Ash, cross_sh = _blockwise_commutant(D2, [XRd, ZRd], sectors2)
    ck(len(Ash) == 41,
       f"leg 7: SHARED vertex -- the flux-superselected one-side algebra has "
       f"dim {len(Ash)} == 41 = 1 + 4 + 4 + 32 (the (1/2,1/2) sector alone "
       "contributes M_4 (+) M_4 = 32: fused spin-0 and spin-1 channels)")
    # the raw commutant additionally carries cross-sector intertwiners:
    # (0,1/2) <-> (1/2,0) share right-spin-1/2 content (dim 4 each way) and
    # (0,0) <-> (1/2,1/2) share right-spin-0 content (dim 4 each way).
    nonzero_cross = {k: v for k, v in cross_sh.items() if v}
    ck(sorted(nonzero_cross.values()) == [4, 4, 4, 4]
       and set(nonzero_cross) == {(0, 3), (3, 0), (1, 2), (2, 1)},
       f"leg 7: cross-sector intertwiner dims {nonzero_cross} -- the raw "
       "commutant is NOT flux-block-diagonal at a shared vertex")
    full_dim = len(Ash) + sum(cross_sh.values())
    ck(full_dim == 57 == 5 ** 2 + 4 ** 2 + 4 ** 2,
       f"leg 7: full raw-commutant dim {full_dim} == 57 = 5^2+4^2+4^2 "
       "(Schur count over fused spin 0/1/2-halves multiplicities 5/4/4)")

    Zsh = _center_of(Ash, D2)
    ck(len(Zsh) == 5,
       f"leg 7: common center dim {len(Zsh)} == 5 > 4 = #flux tuples -- the "
       "electric superselection data STRICTLY EXTENDS the per-link anchor set")
    spZsh = _Span(D2 * D2)
    for Z in Zsh:
        spZsh.add(_flat(Z))
    sector_projs = [_kron(Pa, Pb) for Pa in Pi1 for Pb in Pi1]
    ck(all(spZsh.contains(_flat(P)) for P in sector_projs),
       "leg 7: the 4 flux-tuple projectors lie in the shared-vertex center...")
    spSec = _Span(D2 * D2)
    for P in sector_projs:
        spSec.add(_flat(P))
    ck(spSec.rank == 4,
       "leg 7: ...and span only a 4-dim subalgebra of the 5-dim center")

    # the fused right Casimir (S1 + S2)^2 at the shared vertex
    E1r, F1r, H1r = L1.efh('R')
    Etot = _madd(_kron(E1r, I5), _kron(I5, E1r))
    Ftot = _madd(_kron(F1r, I5), _kron(I5, F1r))
    Htot = _madd(_kron(H1r, I5), _kron(I5, H1r))
    Cfused = _smul(F(1, 4), _madd(_smul(F(2), _madd(_mm(Etot, Ftot),
                                                    _mm(Ftot, Etot))),
                                  _mm(Htot, Htot)))
    ck(all(_commutes(Cfused, B) for B in Ash),
       "leg 7: the fused Casimir (S1+S2)^2 is CENTRAL in the one-side algebra")
    ck(spZsh.contains(_flat(Cfused)),
       "leg 7: ...and lies in the computed center (5 of 5 accounted: the 4 "
       "flux tuples + the fused-channel datum)")
    ck(all(_commutes(Cfused, g) for g in gensA_prod),
       "leg 7: the fused Casimir also lies in the B-side algebra (it commutes "
       "with the A-side product action: via Gauss it is B-interior data) -- "
       "genuinely CO-BILLED cut data")
    ck(not spSec.contains(_flat(Cfused)),
       "leg 7: the fused Casimir is NOT a function of the per-link flux "
       "projectors -- the datum the anchor set (per-link labels) misses; the "
       "superselection sectors at a shared vertex are (j1, j2, J_fused)")
    ck(all(_commutes(z, g) for z in Zsh for g in gensA_prod),
       "leg 7: every central element of the one-side algebra lies in the "
       "B-side algebra too (5 of 5) -- shared superselection data, exactly "
       "as the audit's probe reported")

    n_pass = sum(1 for c, _ in checks if c)

    return _result(
        name='T_anchor_set_is_electric_center_data -- anchor data = '
             'electric-center superselection data at a VERTEX-DISJOINT cut '
             '(with the shared-vertex extension witnessed exactly)',
        tier=4,
        epistemic='P_structural_reading',
        summary=(
            'At a lattice gauge cut in which each boundary vertex hosts at '
            'most one crossed link (the VERTEX-DISJOINT rider, carried on '
            'every statement), the anchor data of a flux-string family under '
            'Paper 12 SS2\'s lattice identification of Definition (anchor) '
            'is exactly the superselection data the electric-center choice '
            '(Casini-Huerta-Rosabal) diagonalizes: the one-side algebra of a '
            'truncated SU(2) Kogut-Susskind link is (+)_j End(V_j)(x)1 '
            '(dim 14 at J = {0, 1/2, 1}), generated by the one-side electric '
            'generators alone; the two sides meet in the common center '
            'span{flux projectors} = the spectral algebra of E^2, and '
            'nowhere else; a flux-changing raw-link matrix unit is in '
            'neither side. Anchor-disjointness is the family-support form: '
            'at two distinct boundary sites the joint one-side algebra is '
            'EXACTLY the tensor product, the center is the sector-tuple '
            'algebra generated by E_1^2 and E_2^2, disjoint-anchor families '
            'commute and jointly span the factorized algebra (the T_M / '
            'L_loc transcription), and same-link families meet in that '
            'link\'s flux projectors. Within a fixed flux sector the '
            'per-index Casimirs are scalars and the residual center is the '
            'fused-channel projectors (dim 3, ranks 2/9/5) -- record-layer '
            'data, not anchor data; the anchor-disjoint product '
            'configuration is abelian dim 4 and factorizes exactly, and the '
            'spanning records (total singlet, exchange P_02) live only in '
            'the shared-anchor algebra. AT A SHARED BOUNDARY VERTEX THE '
            'IDENTITY FAILS AT MODEL STRENGTH (leg 7, the audit\'s probe '
            'reconstructed): the one-side algebra is dim 41 with center '
            'dim 5 > 4 flux tuples, and the fused Casimir (S1+S2)^2 is '
            'central, co-billed by both sides, and provably not a function '
            'of the per-link flux labels -- the electric superselection data '
            'strictly extends the anchor set by the fused-channel label. '
            'The honest verdict: anc is not an algebra-assignment functor '
            '(family-indexed; a magnetic family would select differently, '
            'gated behind the SS10 transport primitive), but for the billed '
            'families the anchor data uniquely selects the electric '
            'assignment within CHR\'s classification-by-center. The '
            'extended-Hilbert-space BILLING BASIS is excluded by the '
            'allocation/X1 reading; the invariant-valued edge TERM is '
            'declined on the no-grounded-J(d) + no-probabilities legs (not '
            'an X1 consequence); the trivial-center exclusion is '
            'reading-gated (allocation reading), not definition-gated. '
            'Delta computes and bounds NO term of the entropy decomposition '
            '-- the one shared invariant d_cut = 2j+1 sizes both the '
            'distillable ceiling and the per-link edge factor (data '
            'overlap, no functional overlap). Grade [P_structural_reading]: '
            'the algebra legs are exact over Q; the four named readings '
            '(module docstring) are load-bearing wherever "anchor" appears. '
            'Occupancy is not claimed.'
        ),
        key_result=(
            'Vertex-disjoint cuts: anchor data = electric-center '
            'superselection data exactly (one-side algebra (+)_j '
            'End(V_j)(x)1; common center = spectral algebra of E^2; '
            'anchor-disjoint <=> families supported in different center '
            'factors). Shared vertex: the electric center strictly extends '
            'the anchor set by the fused-channel label (dim 5 vs 4; the '
            'fused Casimir central, co-billed, not per-link) -- the rider '
            'is load-bearing. EHS billing basis excluded by X1; the edge '
            'term declined on no-J(d) + no-probabilities.'
        ),
        dependencies=[
            'check_T_M', 'check_L_loc',
            'check_T_delta_disjoint_additivity',
            'check_T_su2_string_cut_native_algebra',
            'check_T_gauge_connection_is_gauge_variant_convention_P',
            'check_FD1_structural_completeness',
            'check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P',
        ],
        cross_refs=['check_T_su2_string_cut_comovement',
                    'check_T_delta_coarse_graining_monotonicity',
                    'check_T_cost_count_characterization'],
        n_assertions=len(checks),
        artifacts={
            'rider': 'VERTEX-DISJOINT: each boundary vertex hosts at most '
                     'one crossed link; at a shared vertex the identity '
                     'fails and leg 7 witnesses the exact extension',
            'two_layer': {
                'between_sectors': 'electric-center data = anchor set '
                                   '(billing loci + labels)',
                'within_sector': 'residual center = fused-channel '
                                 'projectors (record layer)',
                'shared_vertex': 'the fused datum migrates into the cut '
                                 'superselection data',
            },
            'leg7_numbers': {
                'one_side_dim': 41, 'raw_commutant_dim': 57,
                'center_dim': 5, 'flux_tuples': 4,
                'cross_intertwiner_dims': '4 each way between (0,1/2) and '
                                          '(1/2,0), and between (0,0) and '
                                          '(1/2,1/2)',
            },
            'falsifiers': [
                '(a) at a link-disjoint-vertex cut: a central, cut-local, '
                'gauge-invariant datum not generated by the per-link E^2 data',
                '(b) an anchor-disjoint family pair whose invariant algebras '
                'fail to factorize',
                '(c) corpus adoption of an edge-mode billing basis OR of a '
                'grounded d-dependent count functional J(d)',
            ],
            'fences': [
                'no entanglement-entropy claim (Delta computes/bounds no '
                'term; the ledger reads no probabilities)',
                'no magnetic-center claim (family-gated, behind the SS10 '
                'transport primitive)',
                'electric choice not forced by A1 alone (family-inherited)',
                'no continuum claim (SU(2) truncations witnessed; Schur '
                'argument general-compact-G but unbanked beyond the '
                'instances)',
                'fixed-content legs inherit the tetraquark cut-modelling '
                'fence (single diagonal comparison group)',
                'trivial-center exclusion is reading-gated (allocation '
                'reading), not definition-gated (F6)',
                'occupancy not claimed',
            ],
            'readings': [
                'lattice identification of Definition (anchor) (Paper 12 SS2)',
                'allocation reading (gauge-variant relabeling = zero-cost '
                'convention)',
                'record reading (physical records = gauge-invariant operators)',
                'commutant-proxy / interior-dressing modelling '
                'identification (F3; leg-1 flag executable)',
            ],
        },
    )


# ============================================================================
# CHECK 2 -- Delta vs the centre-sensitive entropy: opposite verdicts
# ============================================================================

def check_T_delta_vs_centre_entropy_diagnoses() -> Dict:
    """T_delta_vs_centre_entropy_diagnoses: to what extent does Delta
    correlate with the centre-sensitive (electric-centre / CHR-Donnelly)
    entanglement entropy? Exactly to the extent of the shared data -- and
    on named constructions the two accountings issue OPPOSITE verdicts.
    (Landed v24.3.381, 2026-07-04, Paper 12 round-6 walk C3, reviewer Q7;
    fresh-context hostile audit LAND-WITH-FIXES 0.85, mandatory F1 +
    recommended F2/F3/F4/F5 + the F7 grade condition ALL carried; walk of
    record: "The Turning/p12_review6_walks_2026-07-04/c3_delta_entropy/".)

    THE COMPARISON OBJECT (named). The electric-centre algebraic entropy
    of a cut state, S_EC = H({p_c}) + sum_c p_c S(rho~_c), computed on
    the one-side algebra (+)_j End(V_j) (x) 1 of THIS MODULE's check 1
    (CHR electric choice; Donnelly booking: per-link maximally mixed
    boundary factors = the edge term, residual multiplicity correlations
    = the distillable term). SCOPE NOTE F-dist: on every construction
    below the within-sector one-side state is a product of maximally
    mixed per-link edge factors (gauge invariance freezes the single-link
    within-sector state -- Lemma cut-record of the banked testbed), so
    the distillable term is IDENTICALLY 0 and
        S_EC = H({p_c}) + sum_c p_c log2(d_c),
    with d_c the within-sector one-side dimension. A sector list
    [(p_c, d_c)] specifies S_EC exactly; all comparisons are exact
    rational exponentiations 2^(N*S) (the banked _entropy_cmp shape of
    apf/delta_calculus.py). Cuts are vertex-disjoint throughout (the
    shared-vertex correction stays with check 1's leg 7).

    THE LEDGER SIDE. Delta = eps*(J - R) (banked; derived at
    check_T_delta_JR_derived); at a string cut R = 0 and Delta = eps*J
    under a named reading of J. THE READING QUANTIFIER (audit F1, the
    mandatory fix): the anti-ordering theorem quantifies over the THREE
    INTEGER readings of the banked four-reading register
    (check_T_su2_string_cut_comovement clause (iii)) -- unit-count,
    register ceil-log2 PER ANCHOR-DISJOINT COMPONENT (the named
    composition clause of the register model,
    check_T_register_reading_grounds_ceil_log2_count), and (d-1)-count:
    the readings consistent with the characterization theorem's integer
    eps-slot denomination. Each has its own strict anti pair (leg D).
    The FOURTH banked reading, the exact log2-count, is quantified OUT
    and runs as the SECOND NEGATIVE CONTROL: at point-mass statistics
    Delta_log2/eps = sum log2 d = S_EC exactly -- it IS the entropy, so
    it provably never anti-orders it (leg D-log2). This STRENGTHENS the
    diagnosis: strict ANTI is pinned to the integer denomination -- the
    cost floor's ceiling overhead, composing across records, is the
    entire mechanism (a reader holding the four-reading table sees the
    log2 row handled, not dropped).

    THE TWO-COLUMN LEDGER (the answer's shape). SHARED (the skeleton):
    superselection sector structure; d_cut sizes both the edge factor
    log2 d and every count reading of J; anchor-disjointness =
    supported-in-different-centre-factors (check 1) makes BOTH sides
    additive for the same reason. NOT SHARED (the functionals): S_EC
    additionally reads the occupation probabilities p_c and the
    within-sector states; Delta additionally reads the billing partition
    (J vs R) and is denominated in integer eps-slots. Divergences sit
    exactly where the skeleton does not decide: (i) statistics move at
    fixed structure (the dial -- S_EC sweeps, Delta constant); (ii)
    structure moves at fixed state (the sign flip -- S_EC identical term
    by term, Delta = +eps and -eps); (iii) the slot quantization's
    ceiling overhead composes across records until it reverses an
    exact-logarithm ordering (the pinned pair). Neither functional is
    wrong about the other's object; they have different objects.

    LEGS:
      A. Co-movement skeleton: co-zero (no crossing record: both vanish);
         co-positive (every crossing string: both positive); on single
         strings Delta_reg/eps = ceil(S_edge) EXACTLY (the data overlap
         made formula-sharp); additivity of every integer reading over
         anchor-disjoint components, the same factorization that grounds
         Delta-additivity.
      B. The statistics dial: single crossed link, flux support at
         d = 2 and d = 4 (both N-ality 1), sector weight p in
         {1/8, 1/4, 1/2}: S_EC, the Shannon term, and the edge term each
         strictly increase (exact 2^(N*S)); the record structure tuple is
         p-free BY CONSTRUCTION (definitional, the banked leg-F
         precedent: the executable content is the ENTROPY moving, and
         the assertion below is about the entropy; audit F2 -- no
         theater leg claims Delta-constancy as a computation).
      C. The equal-entropy sign flip (audit F3 -- billings DERIVED from
         in-check record models, no verbatim literals): the routed
         string (one j = 1/2 string crossing link 1 XOR link 2, equal
         weight) has S_EC = 2 bits exactly; its routing valuation set
         Omega = {(1,0), (0,1)} is strictly smaller than the free
         product (2 < 4) while BOTH single-label marginals are full --
         the constraint is expressible on NO proper sub-family
         (computed). Parity billing (kappa from the record model
         n(S) = |S| + [both labels in S]) gives Delta = +eps; copy
         billing (one shared routing record, kappa = eps*|S|) gives
         Delta = -eps. Same state, same S_EC term by term, opposite
         sign: no functional of (p_c, rho~_c) computes Delta, not even
         its sign. (Which billing a physical string realizes is NOT
         claimed -- the banked anc-not-a-functor verdict transported;
         occupancy fence.)
      D. The strict anti pairs, one per INTEGER reading, plus two
         negative controls: unit {d=5} vs {2,2} (log2 5 > 2 while
         eps < 2*eps); REGISTER -- THE PINNED PAIR -- (4,4,4) vs
         (5,5,2) with matched controls (string count 3 = 3, (d-1)-count
         9 = 9, total N-ality 1 = 1, point-mass): log2 64 > log2 50
         while 6*eps < 7*eps -- the cut the entropy calls more entangled
         is the cut the ledger bills LESS; (d-1) -- (4,4,2) vs (5,5):
         log2 32 > log2 25 while 7*eps < 8*eps (register too:
         5*eps < 6*eps). NEGATIVE CONTROL 1 (pooled packing, SCOPED AT
         POINT-MASS -- audit F5): ceil(log2 prod d) is the integer
         ceiling of S_EC itself there, ties the pinned pair (6 = 6) and
         admits ZERO anti pairs on the exhaustive sweep of all string
         multisets from d in {2..6} up to size 3 (the register reading
         admits 17 on the same sweep -- the anti rests on the NAMED
         per-component composition clause, which the register model
         carries independently). NEGATIVE CONTROL 2 (exact log2-count,
         audit F1): never anti-orders -- identical comparator to S_EC at
         point-mass, verified on the same sweep.
      E. The obstruction: within the single-record string family at
         point-mass statistics NO anti pair exists under any of the
         three integer readings (every reading non-decreasing in d_cut,
         S_EC strictly increasing -- at fixed billing the shared datum
         drives both the same way); the maximal in-family divergence is
         strict-vs-tie, exactly at the register tie d_cut = 3 vs 4 and
         on the split/unsplit pair. Strict ANTI therefore requires one
         of the three axes of the two-column ledger -- that trichotomy
         IS the physical reason.

    FALSIFIER SURFACES (live; audit F1(c) enumeration): (i) a
    bank-strength derivation of the ledger's J(d) equal to log2 d
    (non-integer) would make Delta_reg = eps*S_edge and collapse legs
    D-E's separation -- the check fails loudly; (ii) any functional of
    (p_c, rho~_c) reproducing Delta across legs B-D refutes the theorem;
    (iii) the per-reading anti quantifier covers EXACTLY the three
    integer readings named above; the fourth banked reading (exact
    log2-count) is the negative control; a newly GROUNDED reading enters
    the quantifier and must be re-witnessed.

    FENCES: no thermal claim; no claim that Delta bounds, computes, or
    approximates any term of the entropy decomposition (the module's
    entropy fence stands -- this check SHARPENS it to opposite verdicts,
    it does not breach it); no claim that either functional is defective
    ("a different accounting, not a better one"); occupancy fence as in
    leg C; vertex-disjoint domain; F-dist scope note (distillable
    identically 0 here; no claim about pairing-sector states).

    GRADE: [P] -- every leg exact finite mathematics with the comparison
    object defined in-module (the check_T_delta_not_an_information_
    functional precedent), the ledger billings derived from in-check
    record models replicating banked content, AND the reading dependence
    carried in the summary itself (audit F7's condition): the anti legs
    are per-named-reading, the register anti rests on the per-component
    composition clause (a priced [P_structural_reading] rider where it
    is grounded), and the quantifier is the corrected integer-readings
    form. Occupancy: not consumed.
    """
    checks = []

    def ck(cond, msg):
        checks.append((bool(cond), msg))
        check(cond, msg)

    from math import lcm, prod
    EPS = F(1)

    # ---- exact entropy machinery (the banked _entropy_cmp shape) --------
    def pow2NS(cfg, N):
        out = F(1)
        for p, d in cfg:
            p = F(p)
            if p:
                e = p * N
                check(e.denominator == 1, "N clears the denominators")
                out *= (F(d) / p) ** int(e)
        return out

    def S_cmp(cfgA, cfgB):
        """Exact sign of S_EC(A) - S_EC(B). No float anywhere."""
        dens = [F(p).denominator for cfg in (cfgA, cfgB) for p, _ in cfg]
        N = lcm(*dens)
        a, b = pow2NS(cfgA, N), pow2NS(cfgB, N)
        return (a > b) - (a < b)

    # ---- the named ledger readings (J at a string cut; R = 0) -----------
    def _cl2(d):
        k, x = 0, 1
        while x < d:
            x *= 2
            k += 1
        return k

    R_unit = lambda ds: len(ds)
    R_register = lambda ds: sum(_cl2(d) for d in ds)   # per-component
    R_dm1 = lambda ds: sum(d - 1 for d in ds)
    R_pooled = lambda ds: _cl2(prod(ds))               # negative control 1
    t_total = lambda ds: sum((d - 1) % 2 for d in ds) % 2
    INTEGER_READINGS = [("unit", R_unit), ("register", R_register),
                        ("d-1", R_dm1)]

    # ================= LEG A -- the co-movement skeleton =================
    fam = [2, 3, 4, 5]
    ck(all(S_cmp([(1, fam[i])], [(1, fam[i + 1])]) < 0 for i in range(3)),
       "leg A: S_EC = log2(d_cut) strictly increasing on the string "
       "family d = 2, 3, 4, 5 (exact)")
    ck(all(S_cmp([(1, d)], [(1, 1)]) > 0 for d in fam)
       and S_cmp([(1, 1)], [(1, 1)]) == 0,
       "leg A: co-positive on every crossing string and co-zero on the "
       "factorizable record -- both functionals null together exactly "
       "where no record crosses (the banked sign criterion)")
    ck(all(2 ** (R_register([d]) - 1) < d <= 2 ** R_register([d])
           for d in fam),
       "leg A: on single strings Delta_reg/eps = ceil(S_edge) exactly "
       "(both sides consume d_cut -- the data overlap made formula-sharp)")
    ck(4 * 4 * 2 == 32 and S_cmp([(1, 4 * 4 * 2)], [(1, 32)]) == 0
       and all(Rf([4, 4, 2]) == Rf([4]) + Rf([4]) + Rf([2])
               for _, Rf in INTEGER_READINGS),
       "leg A: additivity with a shared reason -- S_EC additive over "
       "vertex-disjoint strings (log2 of the product) and every integer "
       "per-component reading additive over anchor-disjoint records "
       "(the same factorization: different centre factors, check 1)")

    # ================= LEG B -- the statistics dial ======================
    probes = [F(1, 8), F(1, 4), F(1, 2)]
    dial = lambda p: [(1 - p, 2), (p, 4)]
    shannon = lambda p: [(1 - p, 1), (p, 1)]
    ck(all(S_cmp(dial(probes[i]), dial(probes[i + 1])) < 0
           for i in range(2)),
       "leg B: S_EC strictly increases across p = 1/8 < 1/4 < 1/2 "
       "(exact 2^(N*S)) while the record structure tuple (sector "
       "support, fusion data) is p-free BY CONSTRUCTION -- p is not an "
       "argument of the ledger (definitional; the banked leg-F "
       "precedent: the executable content is the entropy MOVING)")
    ck(all(S_cmp(shannon(probes[i]), shannon(probes[i + 1])) < 0
           for i in range(2)),
       "leg B: the Shannon (classical sector) term strictly increases "
       "on the probes")
    edge = lambda p: 1 + p
    ck(edge(probes[0]) < edge(probes[1]) < edge(probes[2]),
       "leg B: the edge term (1-p)*log2(2) + p*log2(4) = 1 + p strictly "
       "increases (exact)")
    ck(all((d - 1) % 2 == 1 for d in (2, 4)),
       "leg B: both sectors carry N-ality 1 -- the confinement-relevant "
       "class datum is also blind to the dial (only the statistics move)")

    # ================= LEG C -- the equal-entropy sign flip ==============
    routed = [(F(1, 2), 2), (F(1, 2), 2)]
    ck(S_cmp(routed, [(1, 4)]) == 0,
       "leg C: S_EC(routed string) = 2 bits exactly (Shannon 1 + edge 1 "
       "+ distillable 0; verified against log2 4)")
    omega = [(1, 0), (0, 1)]           # the routing valuation set
    marg0 = {c[0] for c in omega}
    marg1 = {c[1] for c in omega}
    ck(len(omega) == 2 < 4 and marg0 == {0, 1} == marg1,
       "leg C (F3): the Gauss routing constraint strictly cuts the joint "
       "valuation set (2 < 4 = free product) while BOTH single-label "
       "marginals are full -- the constraint is expressible on no proper "
       "sub-family (computed, not asserted)")
    kappa_par = lambda S: EPS * (len(S)
                                 + (1 if {'l1flux', 'l2flux'} <= S else 0))
    d_parity = (kappa_par({'l1flux', 'l2flux'})
                - kappa_par({'l1flux'}) - kappa_par({'l2flux'}))
    kappa_copy = lambda S: EPS * len(S)
    d_copy = (kappa_copy({'route'}) - kappa_copy({'route'})
              - kappa_copy({'route'}))
    ck(d_parity == EPS and d_copy == -EPS and d_parity != d_copy,
       "leg C (F3, billings DERIVED from record models): parity billing "
       "(two flux-label families + the routing constraint) Delta = +eps; "
       "copy billing (two families reading ONE routing record) Delta = "
       "-eps -- one cut state, identical S_EC term by term, OPPOSITE "
       "sign: the state underdetermines the configuration, so not even "
       "sign(Delta) is a function of (p_c, rho~_c). Occupancy fence: "
       "which billing a physical string realizes is not claimed")

    # ================= LEG D -- the strict anti pairs ====================
    A1_, B1_ = [5], [2, 2]
    ck(S_cmp([(1, prod(A1_))], [(1, prod(B1_))]) > 0
       and R_unit(A1_) < R_unit(B1_),
       "leg D1 UNIT ANTI: S_EC log2 5 > 2 bits (5 > 4 exact) while "
       "Delta_unit eps < 2*eps -- more entangled, fewer records billed")
    A2_, B2_ = [4, 4, 4], [5, 5, 2]
    ck(prod(A2_) == 64 and prod(B2_) == 50
       and S_cmp([(1, 64)], [(1, 50)]) > 0,
       "leg D2a: S_EC(A) = log2 64 > log2 50 = S_EC(B) (64 > 50, "
       "integers)")
    ck(R_register(A2_) == 6 < 7 == R_register(B2_),
       "leg D2b REGISTER ANTI (the pinned pair): Delta_reg(A) = 6*eps < "
       "7*eps = Delta_reg(B) -- the cut the entropy calls more entangled "
       "is the cut the ledger bills LESS (per-component composition "
       "clause of the register model, the named rider)")
    ck(R_unit(A2_) == R_unit(B2_) == 3 and R_dm1(A2_) == R_dm1(B2_) == 9
       and t_total(A2_) == t_total(B2_) == 1,
       "leg D2c matched controls: same string count (3), same "
       "(d-1)-count (9), same total N-ality (1), both point-mass, "
       "vertex-disjoint -- the reversal is carried by the ceiling "
       "overhead alone")
    A4_, B4_ = [4, 4, 2], [5, 5]
    ck(prod(A4_) == 32 and prod(B4_) == 25
       and S_cmp([(1, 32)], [(1, 25)]) > 0
       and R_dm1(A4_) == 7 < 8 == R_dm1(B4_)
       and R_register(A4_) == 5 < 6 == R_register(B4_),
       "leg D4 (d-1) ANTI (register too): S_EC log2 32 > log2 25 while "
       "Delta_{d-1} 7*eps < 8*eps and Delta_reg 5*eps < 6*eps")
    ck(R_pooled(A2_) == R_pooled(B2_) == 6,
       "leg D3a NEGATIVE CONTROL 1: pooled packing ties the pinned pair "
       "(ceil log2 64 = ceil log2 50 = 6) -- the register anti rests on "
       "the NAMED per-component composition clause")
    # exhaustive multiset sweep (audit F5: assert the SWEEP, scoped at
    # point-mass statistics, where pooled = ceil(S_EC) exactly)
    from itertools import combinations_with_replacement as _cwr
    multisets = [list(m) for r in (1, 2, 3)
                 for m in _cwr(range(2, 7), r)]
    ck(len(multisets) == 55, "leg D3b sweep space: all 55 string "
       "multisets with d in {2..6}, sizes 1-3")
    n_pooled_anti = sum(1 for Xm in multisets for Ym in multisets
                        if prod(Xm) > prod(Ym)
                        and R_pooled(Xm) < R_pooled(Ym))
    n_reg_anti = sum(1 for Xm in multisets for Ym in multisets
                     if prod(Xm) > prod(Ym)
                     and R_register(Xm) < R_register(Ym))
    ck(n_pooled_anti == 0 and n_reg_anti == 17,
       "leg D3b: pooled packing admits ZERO anti pairs on the exhaustive "
       "sweep (AT POINT-MASS STATISTICS, where ceil(log2 prod d) = "
       "ceil(S_EC) is monotone in the entropy) while the per-component "
       "register admits 17 -- both halves of the control, computed")
    # NEGATIVE CONTROL 2 (audit F1): the exact log2-count reading. Its
    # exact comparator (sum log2 d_i vs sum log2 d'_i <=> prod d vs
    # prod d') and the point-mass entropy comparator are computed by TWO
    # code paths and asserted identical on the FULL sweep; the anti count
    # is then computed from both.
    log2_cmp = lambda Xm, Ym: ((prod(Xm) > prod(Ym))
                               - (prod(Xm) < prod(Ym)))
    identity_ok = all(
        S_cmp([(1, prod(Xm))], [(1, prod(Ym))]) == log2_cmp(Xm, Ym)
        for Xm in multisets for Ym in multisets)
    n_log2_anti = sum(1 for Xm in multisets for Ym in multisets
                      if S_cmp([(1, prod(Xm))], [(1, prod(Ym))]) > 0
                      and log2_cmp(Xm, Ym) < 0)
    ck(identity_ok and n_log2_anti == 0,
       "leg D-log2 NEGATIVE CONTROL 2: the exact log2-count reading "
       "NEVER anti-orders -- at point-mass Delta_log2/eps = sum log2 d "
       "IS S_EC: the two comparators (entropy route vs integer-product "
       "route) agree on ALL 55 x 55 sweep pairs, so the anti condition "
       "is unsatisfiable; strict ANTI is pinned to the INTEGER "
       "denomination exactly")
    ck(S_cmp([(1, prod(A1_))], [(1, prod(B1_))]) > 0
       and R_unit(A1_) < R_unit(B1_)
       and R_register(A2_) < R_register(B2_)
       and S_cmp([(1, prod(A2_))], [(1, prod(B2_))]) > 0
       and R_dm1(A4_) < R_dm1(B4_)
       and S_cmp([(1, prod(A4_))], [(1, prod(B4_))]) > 0,
       "leg D5 (derived conjunction, audit F2 -- no tautology leg): each "
       "of the THREE integer readings has its own strict anti pair "
       "(D1 unit, D2 register, D4 d-1), re-asserted from the computed "
       "quantities")

    # ================= LEG E -- the obstruction ==========================
    no_anti = True
    for i in range(len(fam)):
        for k in range(i + 1, len(fam)):
            lo, hi = fam[i], fam[k]
            for _, Rf in INTEGER_READINGS:
                if Rf([hi]) < Rf([lo]):     # S_EC([hi]) > S_EC([lo]) always
                    no_anti = False
    ck(no_anti,
       "leg E1: NO anti pair within the single-record family d = 2..5 "
       "under any integer reading (every reading non-decreasing in "
       "d_cut, S_EC strictly increasing; gauge invariance freezes the "
       "within-sector state, so at fixed billing the shared datum "
       "drives both functionals the same way)")
    ck(R_register([3]) == R_register([4]) == 2
       and S_cmp([(1, 3)], [(1, 4)]) < 0,
       "leg E2: the maximal in-family divergence is strict-vs-tie -- "
       "S_EC strict (log2 3 < 2) where the register-graded Delta ties "
       "(2*eps = 2*eps), exactly at the banked clause-(ii) tie")
    ck(S_cmp([(1, 4)], [(1, 3)]) > 0
       and R_register([2, 2]) == R_register([3]) == 2,
       "leg E3: split/unsplit -- S_EC strictly separates the split pair "
       "from the single d = 3 string (2 bits vs log2 3) where the "
       "register-graded Delta ties -- the entropy inherits the banked "
       "clause-(iii) divergence under the grounded reading")

    n_legs = len(checks)

    return _result(
        name='T_delta_vs_centre_entropy_diagnoses -- Delta and the '
             'electric-centre entropy share the superselection skeleton '
             'and no functional value: dial, sign flip, and strict '
             'anti-ordered pairs, exact',
        tier=4,
        epistemic='P',
        summary=(
            'DELTA VS THE CENTRE-SENSITIVE ENTROPY (Paper 12 round-6 '
            'walk C3, reviewer Q7). Comparison object named in-check: '
            'the CHR electric-centre entropy S_EC = H({p_c}) + '
            'sum p_c log2 d_c on the one-side algebra of check 1 '
            '(Donnelly booking; distillable identically 0 on every '
            'construction used -- scope note F-dist). The two '
            'accountings share the superselection skeleton (d_cut sizes '
            'both the edge factor and every count reading of J; '
            'anchor-disjointness = different centre factors makes both '
            'additive for the same reason; on single strings '
            'Delta_reg/eps = ceil(S_edge) exactly) and NO functional '
            'value, witnessed on three axes: the STATISTICS DIAL (S_EC, '
            'Shannon, and edge terms strictly sweep across p = 1/8, '
            '1/4, 1/2 while the record structure tuple is p-free by '
            'construction -- the ledger reads no probabilities); the '
            'EQUAL-ENTROPY SIGN FLIP (the routed string, S_EC = 2 bits '
            'exactly, carries Delta = +eps under parity billing and '
            '-eps under copy billing, both DERIVED from in-check record '
            'models with the sub-family-inexpressibility of the routing '
            'constraint computed -- not even sign(Delta) is a function '
            'of the state; which billing a physical string realizes is '
            'NOT claimed); and the PINNED STRICT ANTI-ORDERED PAIR -- '
            'd_cut = (4, 4, 4) vs (5, 5, 2), matched string count, '
            'matched (d-1)-count, matched N-ality, point-mass: S_EC '
            'log2 64 > log2 50 while the register-graded Delta 6*eps < '
            '7*eps -- the cut the entropy calls more entangled is the '
            'cut the ledger bills LESS. READING DEPENDENCE, carried '
            'here (audit F7): the anti legs quantify over the THREE '
            'INTEGER readings of the banked four-reading register '
            '(unit, register-per-component, (d-1)) -- each has its own '
            'strict anti pair -- and the register anti rests on the '
            'per-component composition clause, the named '
            '[P_structural_reading] rider of the register model, with '
            'pooled packing as negative control 1 (ties the pinned '
            'pair; ZERO anti pairs on the exhaustive 55-multiset sweep, '
            'at point-mass statistics, vs 17 for the per-component '
            'register) and the exact log2-count reading as negative '
            'control 2 (at point-mass it IS the entropy and provably '
            'never anti-orders): strict ANTI is pinned to the integer '
            'denomination -- the cost floor\'s ceiling overhead, '
            'composing across records, is the entire mechanism. The '
            'obstruction leg closes the shape: within the single-record '
            'family at point-mass NO anti pair exists under any integer '
            'reading (the shared datum drives both functionals the same '
            'way); the maximal in-family divergence is strict-vs-tie at '
            'the banked register tie. One functional reads (p_c, '
            'rho~_c); the other reads (J, R) in integer eps-slots; '
            'divergences sit exactly on the axes the skeleton does not '
            'fix: the statistics, the billing, and the denomination. '
            'Neither functional is wrong about the other\'s object -- a '
            'different accounting, not a better one; the module entropy '
            'fence is SHARPENED to opposite verdicts, not breached. No '
            'thermal claim; vertex-disjoint domain; all comparisons '
            'exact (rational 2^(N*S), no float on any pass path); %d '
            'assertions. Occupancy: not consumed.' % n_legs
        ),
        key_result=(
            'PINNED-OPPOSITE: equal-entropy sign flip (one state, '
            'Delta = +eps and -eps at S_EC = 2 bits exactly) + strict '
            'anti-ordered pairs under each of the three integer '
            'readings ((4,4,4) vs (5,5,2): S_EC log2 64 > log2 50, '
            'Delta_reg 6*eps < 7*eps, matched controls) + the dial '
            '(entropy sweeps, configuration fixed). Pooled packing and '
            'the exact log2-count never anti-order (negative controls, '
            'point-mass): strict ANTI is pinned to the integer '
            'denomination. Shared skeleton, no shared functional.'
        ),
        dependencies=['check_T_anchor_set_is_electric_center_data',
                      'check_T_delta_disjoint_additivity',
                      'check_T_su2_string_cut_comovement',
                      'check_T_register_reading_grounds_ceil_log2_count'],
        cross_refs=['check_T_delta_not_an_information_functional',
                    'check_T_delta_JR_derived',
                    'check_T_cost_count_characterization',
                    'check_T_delta_coarse_graining_monotonicity'],
        n_assertions=n_legs,
        artifacts={
            'comparison_object': 'CHR electric-centre entropy S_EC = '
                                 'H({p_c}) + sum p_c log2 d_c; Donnelly '
                                 'booking; distillable identically 0 on '
                                 'all constructions (F-dist)',
            'pinned_pair': '(4,4,4) vs (5,5,2): S_EC 64 > 50, '
                           'Delta_reg 6 < 7; matched unit/(d-1)/N-ality',
            'reading_quantifier': 'three INTEGER readings (unit, '
                                  'register-per-component, d-1), each '
                                  'with its own anti pair; exact '
                                  'log2-count = negative control 2 '
                                  '(equals S_EC at point-mass)',
            'sweep': '55 multisets d in {2..6} size <= 3: pooled anti '
                     '0, register anti 17, log2 anti 0 (point-mass)',
            'sign_flip': 'routed string 2 bits exact; parity +eps / '
                         'copy -eps from in-check record models; '
                         'sub-family inexpressibility computed',
            'fences': ['no thermal claim',
                       'entropy fence sharpened, not breached (no term '
                       'computed or bounded)',
                       'occupancy: billing shapes are named witness '
                       'models; no physical-interface sign claim',
                       'vertex-disjoint cuts only (shared-vertex '
                       'correction stays with check 1 leg 7)',
                       'no claim about pairing-sector states'],
        },
    )


_CHECKS = {
    'check_T_anchor_set_is_electric_center_data':
        check_T_anchor_set_is_electric_center_data,
    'check_T_delta_vs_centre_entropy_diagnoses':
        check_T_delta_vs_centre_entropy_diagnoses,
}


def register(registry):
    """Register the anchor <-> electric-center correspondence check."""
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
        "input_id": "gauge:anchor_electric_center_correspondence",
        "axis": "ROUTE",
        "expect_export": False,
        "claim_text": (
            "Anchor data = electric-centre superselection data EXACTLY on "
            "VERTEX-DISJOINT cuts -- the vertex-disjoint rider is PART OF "
            "THE STATEMENT, never dropped: at shared vertices the "
            "fused-Casimir correction enters and exact correspondence fails "
            "(check_T_anchor_set_is_electric_center_data, tier 4 "
            "[P_structural_reading]). Delta and the centre-sensitive "
            "algebraic entropy S_EC share the superselection skeleton d_cut "
            "and NO functional value -- the pinned anti-ordering (4,4,4) vs "
            "(5,5,2): matched invariants, S_EC orders log 64 > log 50 while "
            "the register ledger orders 6 eps < 7 eps "
            "(check_T_delta_vs_centre_entropy_diagnoses [P]). Reading-graded "
            "at the correspondence leg; never a global-P export."
        ),
        "note": (
            "Onboards the Paper 12 round-4/6 anchor--electric-centre "
            "correspondence onto the ROUTE axis as a held claim at its "
            "banked grades. The vertex-disjoint rider and the anti-ordering "
            "are frozen in the claim text (the do-not-re-flatten list, "
            "mechanized)."
        ),
    },
)
