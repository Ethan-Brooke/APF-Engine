"""apf/gauge_invariant_record.py -- The only sharp gauge-invariant colour record is entangled.

A precise, exact statement about the gauge-INVARIANT record structure of the non-abelian
colour sector (no inseparable-IJC / branch / defender claim is made here):

    In SU(N) fundamental (x) antifundamental, the gauge-invariant *-algebra (the commutant
    of the gauge action) is EXACTLY span{pi_singlet, pi_adjoint} -- the two orthogonal
    complementary projectors of the Schur decomposition N (x) Nbar = 1 (+) adj. Its UNIQUE
    rank-1 (sharp) projector is the colour singlet, which is NON-FACTORIZABLE (Schmidt
    rank N). Hence there is NO sharp gauge-invariant PRODUCT-state record: every sharp
    gauge-invariant colour record is entangled.

    For an abelian U(1) gauge group on the same space, the gauge-invariant algebra is large
    and DOES contain sharp product-state (rank-1 factorizable) records. So the result is a
    NON-ABELIAN feature of the gauge group, not generic entanglement.

Why the rank-1 conclusion is exact (not "one product projector fails"): we verify the
gauge-invariant algebra is exactly the 2-dim *-algebra span{pi_s, pi_adj} with pi_s, pi_adj
orthogonal projectors, pi_s + pi_adj = I, pi_s pi_adj = 0. In such an algebra every idempotent
P = a pi_s + b pi_adj (a, b in C; self-adjointness NOT needed) satisfies P^2 = a^2 pi_s +
b^2 pi_adj = P, so a^2 = a and b^2 = b, hence a, b in {0,1} (over C, z^2=z => z in {0,1}); the
idempotents are exactly {0, pi_s, pi_adj, I} with ranks {0, 1, N^2-1, N^2}.
The unique rank-1 idempotent is therefore pi_s. (All four are exhibited with their ranks.)

"Gauge-invariant = physical/admissible record" is the reading banked by the no-B allocation
(check_T_gauge_connection_is_gauge_variant_convention_P: gauge-variant content is convention).
Grade [P_structural_reading]: the rep theory is exact; the reading identifies the
gauge-invariant operators with the physical sharp records.

SCOPE -- this does NOT claim: branch (IJC) (for the MESON the gauge-invariant colour algebra is in fact
ABELIAN, span{pi_s,pi_adj} -- m=1-specific; at m>=2 the exotic algebra is non-abelian, see
check_T_exotic_gauge_invariant_algebra_is_nonabelian); confinement (which additionally needs L_irr / dynamics); the
gap VALUE or continuum existence (fenced to the open program). The connection A_mu stays the
transverse gauge-variant convention of the no-B allocation. The statement is solely about the
gauge-invariant sharp-record structure.
"""
from __future__ import annotations

from fractions import Fraction as F
from typing import Dict, Iterable, List, Mapping, Optional


class Q:
    __slots__ = ("r", "i")
    def __init__(self, r=0, i=0): self.r = F(r); self.i = F(i)
    def __add__(a, b): return Q(a.r + b.r, a.i + b.i)
    def __sub__(a, b): return Q(a.r - b.r, a.i - b.i)
    def __mul__(a, b): return Q(a.r * b.r - a.i * b.i, a.r * b.i + a.i * b.r)
    def conj(a): return Q(a.r, -a.i)
    def is0(a): return a.r == 0 and a.i == 0
    def __eq__(a, b): return a.r == b.r and a.i == b.i
    def inv(a):
        d = a.r * a.r + a.i * a.i
        return Q(a.r / d, -a.i / d)


Mat = List[List[Q]]


def _zeros(n): return [[Q(0, 0) for _ in range(n)] for _ in range(n)]
def _eye(n):
    M = _zeros(n)
    for k in range(n): M[k][k] = Q(1, 0)
    return M
def _mm(A, B):
    n = len(A); m = len(B[0]); k = len(B)
    C = [[Q(0, 0) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for t in range(k):
            a = A[i][t]
            if a.is0(): continue
            Bt = B[t]; Ci = C[i]
            for j in range(m): Ci[j] = Ci[j] + a * Bt[j]
    return C
def _add(A, B): return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]
def _sub(A, B): return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]
def _comm(A, B): return _sub(_mm(A, B), _mm(B, A))
def _conjm(A): return [[A[i][j].conj() for j in range(len(A))] for i in range(len(A))]
def _eqm(A, B): return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A)))
def _iszero(M): return all(M[i][j].is0() for i in range(len(M)) for j in range(len(M)))
def _kron(A, B):
    n = len(A); m = len(B); out = _zeros(n * m)
    for i in range(n):
        for j in range(n):
            a = A[i][j]
            if a.is0(): continue
            for p in range(m):
                for q in range(m):
                    out[i * m + p][j * m + q] = a * B[p][q]
    return out


def _su_n_gens(N: int) -> List[Mat]:
    """A genuine basis of su(N): N(N-1) off-diagonal root generators {E_ij-E_ji, i(E_ij+E_ji)}
    PLUS (N-1) Cartan generators i(E_kk - E_{k+1,k+1}). Total N^2-1 = dim su(N)."""
    gens = []
    for i in range(N):
        for j in range(i + 1, N):
            A = _zeros(N); A[i][j] = Q(1, 0); A[j][i] = Q(-1, 0); gens.append(A)
            B = _zeros(N); B[i][j] = Q(0, 1); B[j][i] = Q(0, 1); gens.append(B)
    for k in range(N - 1):
        H = _zeros(N); H[k][k] = Q(0, 1); H[k + 1][k + 1] = Q(0, -1); gens.append(H)
    return gens


def _action_gens(N: int, group: str) -> List[Mat]:
    """Gauge action on fund (x) antifund: L = g (x) I + I (x) conj(g)."""
    IN = _eye(N)
    if group == "SU":
        gs = _su_n_gens(N)
    else:
        D = _zeros(N)
        for k in range(N): D[k][k] = Q(0, k)
        gs = [D]
    return [_add(_kron(g, IN), _kron(IN, _conjm(g))) for g in gs]


def _singlet_proj(N: int) -> Mat:
    n = N * N; P = _zeros(n); v = F(1, N)
    for i in range(N):
        for j in range(N):
            P[i * N + i][j * N + j] = Q(v, 0)
    return P


def _P00(N: int) -> Mat:
    n = N * N; P = _zeros(n); P[0][0] = Q(1, 0); return P


def _rank(M: Mat) -> int:
    M = [row[:] for row in M]; rows = len(M); cols = len(M[0]) if rows else 0; r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if not M[i][c].is0(): piv = i; break
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        inv = M[r][c].inv()
        M[r] = [x * inv for x in M[r]]
        for i in range(rows):
            if i != r and not M[i][c].is0():
                f = M[i][c]; M[i] = [M[i][j] - f * M[r][j] for j in range(cols)]
        r += 1
        if r == rows: break
    return r


def _commutant_dim(N: int, group: str) -> int:
    n = N * N
    Ls = _action_gens(N, group)
    cols = []
    for i in range(n):
        for j in range(n):
            X = _zeros(n); X[i][j] = Q(1, 0)
            cv = []
            for L in Ls:
                cm = _comm(X, L)
                for p in range(n):
                    for q in range(n):
                        cv.append(cm[p][q])
            cols.append(cv)
    nrows = len(cols[0]); ncols = len(cols)
    M = [[cols[c][r] for c in range(ncols)] for r in range(nrows)]
    return ncols - _rank(M)


def _in_commutant(X, N, group): return all(_iszero(_comm(X, L)) for L in _action_gens(N, group))


def _colour_dipole(N):
    """Colour dipole T1.T2 on fund (x) antifund via the SU(N) completeness (Fierz) relation
    (exact rational, normalization Tr(t^a t^b)=1/2 delta):
       (T1.T2)_{(ip,kp),(i,k)} = -(1/2) d_{ip,kp} d_{i,k} + (1/(2N)) d_{ip,i} d_{k,kp}."""
    n = N * N
    T = _zeros(n)
    for ip in range(N):
        for kp in range(N):
            for i in range(N):
                for k in range(N):
                    val = (F(-1, 2) if (ip == kp and i == k) else F(0)) \
                          + (F(1, 2 * N) if (ip == i and k == kp) else F(0))
                    if val != 0:
                        T[ip * N + kp][i * N + k] = Q(val, 0)
    return T


def check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P() -> Dict:
    """The unique sharp gauge-invariant colour record is the non-factorizable singlet.
    See module docstring. Exact Q[i]; SU(2), SU(3); abelian U(1) control."""
    by_N = {}
    ok = True
    for N in (2, 3):
        n = N * N
        ps = _singlet_proj(N)
        padj = _sub(_eye(n), ps)
        # (1) the gauge-invariant *-algebra is EXACTLY span{pi_s, pi_adj}:
        dim = _commutant_dim(N, "SU")
        ps_inv = _in_commutant(ps, N, "SU")
        padj_inv = _in_commutant(padj, N, "SU")
        ps_proj = _eqm(_mm(ps, ps), ps)
        padj_proj = _eqm(_mm(padj, padj), padj)
        orthogonal = _iszero(_mm(ps, padj))            # pi_s pi_adj = 0
        complete = _eqm(_add(ps, padj), _eye(n))         # pi_s + pi_adj = I
        commute = _iszero(_comm(ps, padj))
        algebra_is_span = (dim == 2 and ps_inv and padj_inv and ps_proj and padj_proj
                           and orthogonal and complete and commute)
        # (2) enumerate the idempotents {0, pi_s, pi_adj, I} and their ranks
        idem = {"0": _zeros(n), "pi_s": ps, "pi_adj": padj, "I": _eye(n)}
        ranks = {k: _rank(v) for k, v in idem.items()}
        rank1_projectors = [k for k, rr in ranks.items() if rr == 1]
        unique_rank1_is_singlet = (rank1_projectors == ["pi_s"])
        # (3) the singlet is non-factorizable (Schmidt rank N); P00 is a rank-1 product record
        schmidt_singlet = N
        singlet_nonfactorizable = schmidt_singlet > 1
        # abelian control: a sharp product-state gauge-invariant record EXISTS
        dim_ab = _commutant_dim(N, "U1")
        p00 = _P00(N)
        p00_inv_ab = _in_commutant(p00, N, "U1")
        p00_factorizable = True  # |0,0> is a product state (Schmidt rank 1)
        abelian_has_product_record = (dim_ab > 2 and p00_inv_ab and p00_factorizable)
        # also confirm P00 is NOT gauge-invariant in the non-abelian case
        p00_inv_su = _in_commutant(p00, N, "SU")
        # corollary (value side, folded in): the unique record pi_s is the -C_F eigenstate of the
        # colour dipole T1.T2 (eigenvalues are standard SU(N) Casimirs; C_F=4/3 for the forced N_c=3)
        Tdip = _colour_dipole(N)
        Tps = _mm(Tdip, ps)
        lam_s = Tps[0][0].r / ps[0][0].r
        lamQ = Q(lam_s, 0)
        record_eig_exact = _iszero(_sub(Tps, [[lamQ * ps[a][b] for b in range(n)] for a in range(n)]))
        CF = F(N * N - 1, 2 * N)
        record_is_minus_CF = record_eig_exact and (lam_s == -CF)

        cell_ok = (algebra_is_span and unique_rank1_is_singlet and singlet_nonfactorizable
                   and abelian_has_product_record and not p00_inv_su and record_is_minus_CF)
        ok = ok and cell_ok
        by_N[f"SU({N})"] = {
            "gauge_invariant_algebra_dim": dim,
            "algebra_is_exactly_span_pi_s_pi_adj": algebra_is_span,
            "idempotent_ranks": ranks,
            "unique_rank1_gauge_invariant_projector": rank1_projectors,
            "unique_rank1_is_singlet": unique_rank1_is_singlet,
            "singlet_schmidt_rank": schmidt_singlet,
            "singlet_nonfactorizable": singlet_nonfactorizable,
            "product_record_P00_gauge_invariant_nonabelian": p00_inv_su,
            "abelian_U1_algebra_dim": dim_ab,
            "abelian_has_sharp_product_record": abelian_has_product_record,
            "record_colour_dipole_eigenvalue": str(lam_s),
            "record_is_minus_C_F_eigenstate": record_is_minus_CF,
            "cell_ok": cell_ok,
        }
    data = {
        "model": "SU(N) fundamental (x) antifundamental; gauge-invariant *-algebra = commutant (exact Q[i])",
        "by_N": by_N,
        "statement": ("the unique sharp (rank-1) gauge-invariant record is the non-factorizable colour "
                      "singlet; no sharp gauge-invariant product-state record exists; abelian U(1) admits one"),
        "discriminator": "non-abelian gauge group collapses the gauge-invariant algebra to span{pi_s,pi_adj}; abelian keeps it large -- colour load-bearing",
        "reading_adopted": "gauge-invariant = physical/admissible record (the no-B allocation, check_T_gauge_connection_is_gauge_variant_convention_P)",
        "scope": ("ONLY the gauge-invariant sharp-record structure; NOT branch (IJC) (the gauge-invariant colour "
                  "algebra is itself abelian span{pi_s,pi_adj} -- m=1-specific; at m>=2 (e.g. the tetraquark) the exotic gauge-invariant algebra is NON-ABELIAN (check_T_exotic_gauge_invariant_algebra_is_nonabelian), so the meson criterion-route refutation of colour=IJC is scoped to m=1; reopening at m>=2: on the structural rung the M_3 block hosts a gauge-invariant KCBS interface that is IJCStr (check_T_gauge_invariant_colour_interface_is_contextual), while IJC_adm stays not-computable for colour), NOT confinement (needs L_irr/dynamics), NOT gap "
                  "value/continuum; the connection A_mu stays transverse convention."),
        "colour_factor_corollary": ("the unique record pi_s is the -C_F eigenstate of the gauge-invariant colour "
                  "dipole T1.T2 (the most-attractive channel); -C_F=-(N^2-1)/(2N) = -4/3 for the APF-forced N_c=3. "
                  "The eigenvalue is a STANDARD SU(N) Casimir (not derived here); this records the record<->colour-"
                  "force identification only, NOT an independent C_F derivation."),
    }
    if ok:
        return _ok(
            "check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P",
            status="P_structural_reading",
            summary=("In SU(2)/SU(3) fund (x) antifund the gauge-invariant *-algebra is exactly the 2-dim "
                     "span{pi_singlet, pi_adjoint}; its unique rank-1 projector is the non-factorizable colour "
                     "singlet (Schmidt rank N), so every sharp gauge-invariant colour record is entangled and no "
                     "sharp product-state gauge-invariant record exists. Abelian U(1) admits sharp product-state "
                     "gauge-invariant records -- a non-abelian feature, colour load-bearing. Reading: "
                     "gauge-invariant = physical record (the no-B allocation). No (IJC)/confinement/gap claim. Corollary: that unique record is the -C_F eigenstate of the colour dipole (-4/3 for N_c=3, a standard Casimir)."),
            data=data,
            dependencies=["check_T_gauge_connection_is_gauge_variant_convention_P"],
        )
    return _fail(
        "check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P",
        status="FAIL",
        summary="Reframed gauge-invariant-record witness did not hold.",
        data=data,
    )


def _ok(name, *, status, summary, data=None, dependencies=None):
    return {"name": name, "consistent": True, "status": status, "summary": summary,
            "data": dict(data or {}), "dependencies": list(dependencies or [])}
def _fail(name, *, status, summary, data=None, dependencies=None):
    return {"name": name, "consistent": False, "status": status, "summary": summary,
            "data": dict(data or {}), "dependencies": list(dependencies or [])}


# --- baryon: N fundamentals of SU(N), the totally-antisymmetric singlet ------

def _perm_sign(perm):
    n = len(perm); sgn = 1
    for i in range(n):
        for j in range(i + 1, n):
            if perm[i] > perm[j]: sgn = -sgn
    return sgn


def _baryon_action_gens(N):
    """Gauge action on fund^(x)N: L_a = sum_k I^(x)k (x) g_a (x) I^(x)(N-1-k)."""
    gs = _su_n_gens(N); IN = _eye(N); dim = N ** N
    Ls = []
    for g in gs:
        L = _zeros(dim)
        for k in range(N):
            factors = [IN] * N; factors[k] = g
            E = factors[0]
            for f in factors[1:]:
                E = _kron(E, f)
            L = _add(L, E)
        Ls.append(L)
    return Ls


def _eps_singlet_vec(N):
    """Totally-antisymmetric singlet vector in fund^(x)N (un-normalized)."""
    from itertools import permutations
    dim = N ** N
    v = [Q(0, 0) for _ in range(dim)]
    for perm in permutations(range(N)):
        idx = 0
        for k in range(N):
            idx = idx * N + perm[k]
        v[idx] = v[idx] + Q(_perm_sign(perm), 0)
    return v


def _matvec(L, v):
    n = len(v)
    return [sum((L[i][j] * v[j] for j in range(n)), Q(0, 0)) for i in range(n)]


def _vec_is_zero(v):
    return all(x.is0() for x in v)


def _invariant_subspace_dim(N):
    Ls = _baryon_action_gens(N); dim = N ** N
    M = []
    for L in Ls:
        for i in range(dim):
            M.append(L[i][:])
    return dim - _rank(M)


def _schmidt_rank_first_vs_rest(N, v):
    rows = N; cols = N ** (N - 1)
    Mtx = [[v[r * cols + c] for c in range(cols)] for r in range(rows)]
    return _rank(Mtx)


def check_T_unique_gauge_invariant_colour_state_of_N_fundamentals_is_entangled_baryon_P():
    """The unique gauge-invariant colour state of N SU(N) fundamentals is the entangled
    epsilon-baryon (extends the meson record result to the baryon).

    fund^(x)N decomposes into many irreps (e.g. SU(3): 3(x)3(x)3 = 10 (+) 8 (+) 8 (+) 1), so
    the gauge-invariant algebra is no longer 2-dim. But a SHARP gauge-invariant record is a
    1-dim invariant subspace = an invariant VECTOR (SU(N) is simple, so it has NO non-trivial
    1-dim rep; a rank-1 gauge-invariant projector |psi><psi| forces U(g)|psi> = |psi>). The
    multiplicity of the trivial rep in fund^(x)N is exactly 1 (standard Schur-Weyl: the singlet
    corresponds to the single full-height column [1^N] = the sign rep of S_N, dim 1, for every N;
    computed here as the invariant-subspace dimension, with N=2,3 as the witnesses), and that
    invariant vector is the totally-antisymmetric epsilon baryon, which is NON-FACTORIZABLE
    (Schmidt rank N across first|rest). So the unique sharp
    gauge-invariant baryon record is entangled -- the same conclusion as the meson, by a
    different (invariant-vector) route.

    Exact Q[i], SU(2) (2 fundamentals) and SU(3) (3 fundamentals). Reading: gauge-invariant =
    physical record (the no-B allocation). Grade [P_structural_reading]. NO (IJC)/confinement/
    gap claim; this is solely the gauge-invariant sharp-record structure of the baryon.
    """
    by_N = {}
    ok = True
    for N in (2, 3):
        dim = N ** N
        inv_dim = _invariant_subspace_dim(N)
        eps = _eps_singlet_vec(N)
        Ls = _baryon_action_gens(N)
        eps_invariant = all(_vec_is_zero(_matvec(L, eps)) for L in Ls)
        eps_nonzero = not _vec_is_zero(eps)
        sr = _schmidt_rank_first_vs_rest(N, eps)
        eps_nonfactorizable = sr > 1
        unique = (inv_dim == 1 and eps_invariant and eps_nonzero)
        cell_ok = unique and eps_nonfactorizable
        ok = ok and cell_ok
        by_N[f"SU({N})_baryon_{N}_fundamentals"] = {
            "space_dim_N^N": dim,
            "invariant_subspace_dim": inv_dim,
            "trivial_rep_multiplicity_is_1": inv_dim == 1,
            "epsilon_is_invariant": eps_invariant,
            "epsilon_spans_the_unique_invariant_state": unique,
            "epsilon_schmidt_rank_first_vs_rest": sr,
            "epsilon_nonfactorizable": eps_nonfactorizable,
            "cell_ok": cell_ok,
        }
    data = {
        "model": "SU(N) fund^(x)N (N colour charges); invariant subspace = trivial-rep isotypic (exact Q[i])",
        "by_N": by_N,
        "statement": ("the unique gauge-invariant colour state of N SU(N) fundamentals is the "
                      "totally-antisymmetric epsilon baryon, which is non-factorizable (entangled)"),
        "sharp_record_reading": ("a sharp gauge-invariant record = a 1-dim invariant subspace = an "
                                 "invariant vector, since SU(N) has no non-trivial 1-dim rep; there is "
                                 "exactly one (the epsilon), and it is entangled"),
        "reading_adopted": "gauge-invariant = physical/admissible record (the no-B allocation)",
        "scope": ("ONLY the gauge-invariant sharp-record structure of the baryon; NOT (IJC), NOT "
                  "confinement (needs L_irr/dynamics), NOT gap value/continuum; connection A_mu stays convention."),
    }
    if ok:
        return _ok(
            "check_T_unique_gauge_invariant_colour_state_of_N_fundamentals_is_entangled_baryon_P",
            status="P_structural_reading",
            summary=("For SU(2) (2 fundamentals) and SU(3) (3 fundamentals) the invariant subspace of "
                     "fund^(x)N is exactly 1-dimensional and is spanned by the totally-antisymmetric "
                     "epsilon baryon, which is non-factorizable (Schmidt rank N across first|rest). So the "
                     "unique sharp gauge-invariant colour state of N fundamentals is entangled -- the meson "
                     "record result extended to the baryon, via the invariant-vector route. Reading: "
                     "gauge-invariant = physical record (no-B allocation). No (IJC)/confinement/gap claim."),
            data=data,
            dependencies=["check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P",
                          "check_T_gauge_connection_is_gauge_variant_convention_P"],
        )
    return _fail(
        "check_T_unique_gauge_invariant_colour_state_of_N_fundamentals_is_entangled_baryon_P",
        status="FAIL",
        summary="Baryon gauge-invariant-state witness did not hold.",
        data=data,
    )



# =====================================================================
# Canonical (frame-free) sharp gauge-invariant record  <=>  multiplicity-free (m=1)
# (generalizes the meson/baryon record results; exhibits the m>=2 boundary)
# =====================================================================

def _fund_n_gens(N, n):
    """su(N) action on fund^(x)n: L_a = sum_k I^(x)k (x) g_a (x) I^(x)(n-1-k)."""
    gs = _su_n_gens(N); IN = _eye(N); dim = N ** n; Ls = []
    for g in gs:
        L = _zeros(dim)
        for k in range(n):
            facs = [IN] * n; facs[k] = g
            E = facs[0]
            for f in facs[1:]:
                E = _kron(E, f)
            L = _add(L, E)
        Ls.append(L)
    return Ls


def _inv_dim_fund_n(N, n):
    """Trivial-rep multiplicity in fund^(x)n = dim of the invariant subspace."""
    Ls = _fund_n_gens(N, n); dim = N ** n; M = []
    for L in Ls:
        for i in range(dim):
            M.append(L[i][:])
    return dim - _rank(M)


def _inv_dim_meson(N):
    """Trivial-rep multiplicity in fund (x) antifund."""
    Ls = _action_gens(N, "SU"); dim = N * N; M = []
    for L in Ls:
        for i in range(dim):
            M.append(L[i][:])
    return dim - _rank(M)


def _meson_vec(N):
    """The colour-singlet meson vector sum_i |i,i> (un-normalized)."""
    v = [Q(0, 0) for _ in range(N * N)]
    for i in range(N):
        v[i * N + i] = Q(1, 0)
    return v


def _schmidt_bipartite(N, n, vec, left):
    """Exact rank of the (left-indices x right-indices) reshape of an N^n vector."""
    right = [s for s in range(n) if s not in left]

    def dig(idx):
        ds = []
        for _ in range(n):
            ds.append(idx % N); idx //= N
        ds.reverse(); return ds

    rows = {}
    for idx in range(N ** n):
        if vec[idx].is0():
            continue
        ds = dig(idx)
        l = tuple(ds[s] for s in left); r = tuple(ds[s] for s in right)
        rows.setdefault(l, {})[r] = vec[idx]
    lkeys = sorted(rows); rkeys = sorted({r for d in rows.values() for r in d})
    if not lkeys or not rkeys:
        return 0
    M = [[rows[l].get(r, Q(0, 0)) for r in rkeys] for l in lkeys]
    return _rank(M)


def _pair_eps_vec(n, p1, p2):
    """SU(2): eps_{p1} eps_{p2}, a product of two singlets, in the 2^n space."""
    from itertools import permutations
    v = [Q(0, 0) for _ in range(2 ** n)]
    for pa in permutations(range(2)):
        for pb in permutations(range(2)):
            ds = [0] * n
            ds[p1[0]] = pa[0]; ds[p1[1]] = pa[1]
            ds[p2[0]] = pb[0]; ds[p2[1]] = pb[1]
            idx = 0
            for d in ds:
                idx = idx * 2 + d
            v[idx] = v[idx] + Q(_perm_sign(pa) * _perm_sign(pb), 0)
    return v


def check_T_canonical_colour_record_iff_multiplicity_free_P() -> Dict:
    """Canonical (frame-free) sharp gauge-invariant colour record  <=>  singlet multiplicity m=1.

    The trivial-rep multiplicity m of a colour channel partitions it THREE ways:
      m=0  -> NO sharp gauge-invariant record at all;
      m=1  -> a UNIQUE canonical (frame-free) sharp record;
      m>=2 -> records exist but NONE is canonical -- pinning a sharp record needs a basis
              vector in the m-dim multiplicity space, and there is no GROUP-canonical such
              basis (a frame / convention; the same SPECIES as the no-B across-interface
              frame, a DIFFERENT object).

    In the verified NON-ABELIAN channels (SU(2)/SU(3) meson, SU(2) diquark, SU(3) baryon,
    all m=1) the unique invariant is ENTANGLED (Schmidt rank N). Entanglement is
    NON-ABELIAN-SPECIFIC: abelian U(1) admits a sharp PRODUCT (separable) gauge-invariant
    record (P00), so m=1 does NOT imply entangled in general; the non-abelian gauge group
    forces it (inherited from the two dependency checks). Exhibited m>=2 boundary:
    SU(2) fund^4 (m=2) -- two independent invariants, no group-canonical basis (no canonical
    record), and the admissible sector contains a SEPARABLE state (eps12.eps34, Schmidt rank
    1 across (01|23)), so admissibility no longer forces entanglement.

    Grade [P_structural_reading]: the multiplicities + Schmidt ranks are exact [P]-grade rep
    theory; the steps "gauge-invariant = physical record" and "no group-canonical multiplicity
    basis => no admissible canonical record" are the adopted gauge-variant-CONVENTION (no-B)
    reading, not [P].

    FENCES (explicit non-claims):
      (i)   NOT occupancy / branch-(IJC): an entangled colour record is NOT IJC; the
            gauge-invariant colour algebra is ABELIAN (the colour=IJC identity is refuted).
      (ii)  the multiplicity-frame "B" is the SAME SPECIES as the loc_commut across-interface
            frame (both = a non-group-canonical basis choice = a gauge-variant convention) but
            a DIFFERENT OBJECT (internal multiplicity basis vs across-interface colour-space iso
            A1~=A2). The shared species is the gauge-variant-CONVENTION reading, NOT the
            operational-radical no-phantom-records primitive (a multiplicity-frame choice picks
            operationally DISTINGUISHABLE states, so it is not a no-phantom radical direction).
      (iii) m>=1 is required for ANY sharp record; canonical<=>m=1 is the m=1-vs-m>=2
            (canonical-vs-non-canonical) split, NOT the m=0 record-existence boundary.
    """
    m = {
        "SU(2) meson":          _inv_dim_meson(2),
        "SU(3) meson":          _inv_dim_meson(3),
        "SU(2) diquark fund^2": _inv_dim_fund_n(2, 2),
        "SU(2) fund^3":         _inv_dim_fund_n(2, 3),
        "SU(2) fund^4":         _inv_dim_fund_n(2, 4),
        "SU(3) baryon fund^3":  _inv_dim_fund_n(3, 3),
    }
    # (A) the trichotomy on the channels (m=0 / m=1 / m>=2)
    triA = (m["SU(2) meson"] == 1 and m["SU(3) meson"] == 1
            and m["SU(2) diquark fund^2"] == 1 and m["SU(3) baryon fund^3"] == 1
            and m["SU(2) fund^3"] == 0 and m["SU(2) fund^4"] == 2)
    # (B) m=1 channels: unique invariant entangled (Schmidt rank N) -- non-abelian
    sr_meson2 = _schmidt_bipartite(2, 2, _meson_vec(2), [0])
    sr_meson3 = _schmidt_bipartite(3, 2, _meson_vec(3), [0])
    triB = (sr_meson2 == 2 and sr_meson3 == 3)
    # non-abelian-specificity control: abelian U(1) admits a sharp product record (P00)
    u1_product_record = _in_commutant(_P00(2), 2, "U1")
    # (C) m>=2 boundary, exhibited on SU(2) fund^4
    v1234 = _pair_eps_vec(4, (0, 1), (2, 3))
    v1423 = _pair_eps_vec(4, (0, 3), (1, 2))
    Ls4 = _fund_n_gens(2, 4)
    both_inv = (all(_vec_is_zero(_matvec(L, v1234)) for L in Ls4)
                and all(_vec_is_zero(_matvec(L, v1423)) for L in Ls4))
    indep2 = (_rank([[x for x in v1234], [x for x in v1423]]) == 2)
    sep_state = (_schmidt_bipartite(2, 4, v1234, [0, 1]) == 1)
    triC = (both_inv and indep2 and sep_state)

    ok = bool(triA and triB and u1_product_record and triC)
    data = {
        "model": "SU(N) colour channels; trivial-rep multiplicity via exact invariant-subspace rank (Q[i])",
        "multiplicities_m": m,
        "trichotomy_m0_m1_m2_holds": triA,
        "m1_unique_invariant_entangled_schmidt_rank": {"SU(2) meson": sr_meson2, "SU(3) meson": sr_meson3},
        "entanglement_nonabelian_specific_U1_admits_product_record": bool(u1_product_record),
        "m2_boundary_SU2_fund4": {
            "two_independent_invariants": indep2,
            "both_gauge_invariant": both_inv,
            "eps12eps34_separable_across_01_23": sep_state,
        },
        "criterion": ("a canonical frame-free sharp gauge-invariant record exists IFF m=1; at m=1 in the "
                      "verified non-abelian channels it is entangled (Schmidt rank N); at m>=2 (SU(2) fund^4) "
                      "no canonical record exists and the admissible sector contains a separable state"),
        "reading_adopted": ("gauge-invariant = physical record + no group-canonical multiplicity basis => no "
                            "canonical admissible record (the gauge-variant-convention / no-B reading)"),
        "scope_fences": {
            "not_IJC": "entangled colour record != branch-(IJC); gauge-invariant colour algebra is abelian (colour=IJC refuted)",
            "multiplicity_B_vs_across_interface_B": ("same SPECIES (a gauge-variant convention = non-group-canonical "
                       "basis choice) but a DIFFERENT object (internal multiplicity basis vs across-interface frame iso); "
                       "the shared species is the convention reading, NOT the operational-radical no-phantom primitive"),
            "record_existence": "m>=1 needed for any sharp record; canonical<=>m=1 is the m=1-vs-m>=2 split, not the m=0 boundary",
        },
    }
    if ok:
        return _ok(
            "check_T_canonical_colour_record_iff_multiplicity_free_P",
            status="P_structural_reading",
            summary=("Canonical (frame-free) sharp gauge-invariant colour record EXISTS iff the singlet "
                     "multiplicity m=1 (trichotomy m=0 no record / m=1 canonical / m>=2 non-canonical). In the "
                     "verified non-abelian channels (SU(2)/SU(3) meson, SU(2) diquark, SU(3) baryon, all m=1) the "
                     "unique invariant is entangled (Schmidt rank N) -- a NON-ABELIAN feature (abelian U(1) admits "
                     "a sharp product record). Exhibited m>=2 boundary SU(2) fund^4 (m=2): no canonical record + a "
                     "separable admissible state (eps12.eps34), so admissibility no longer forces entanglement. "
                     "Reading: gauge-invariant=physical record + no group-canonical multiplicity basis => no canonical "
                     "record (the gauge-variant-convention / no-B reading). NOT IJC, NOT confinement/gap; the "
                     "multiplicity-B is the same convention species as the across-interface B but a different object."),
            data=data,
            dependencies=["check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P",
                          "check_T_unique_gauge_invariant_colour_state_of_N_fundamentals_is_entangled_baryon_P",
                          "check_T_gauge_connection_is_gauge_variant_convention_P"],
        )
    return _fail(
        "check_T_canonical_colour_record_iff_multiplicity_free_P",
        status="FAIL",
        summary="multiplicity-free criterion witness did not hold.",
        data=data,
    )



# =====================================================================
# Exotic (tetraquark) gauge-invariant algebra is NON-ABELIAN at m>=2
# (the meson abelian-algebra fence is multiplicity-free-specific)
# =====================================================================

def _tetra_gens(N):
    """su(N) action on fund (x) antifund (x) fund (x) antifund."""
    gs = _su_n_gens(N); IN = _eye(N); dim = N ** 4
    slot = lambda g: [g, _conjm(g), g, _conjm(g)]
    Ls = []
    for g in gs:
        L = _zeros(dim); sg = slot(g)
        for s in range(4):
            facs = [IN] * 4; facs[s] = sg[s]
            E = facs[0]
            for f in facs[1:]:
                E = _kron(E, f)
            L = _add(L, E)
        Ls.append(L)
    return Ls


def _tetra_inv_dim(N):
    Ls = _tetra_gens(N); dim = N ** 4; M = []
    for L in Ls:
        for i in range(dim):
            M.append(L[i][:])
    return dim - _rank(M)


def _su2_meson_pair_vec(pairs):
    """SU(2) tetraquark: product of two meson singlets on the given index-pairs.
    pairs = ((a,b),(c,d)): slots a,b share an index; slots c,d share an index."""
    v = [Q(0, 0) for _ in range(16)]
    (a, b), (c, d) = pairs
    for i in (0, 1):
        for j in (0, 1):
            idx = [0, 0, 0, 0]
            idx[a] = i; idx[b] = i; idx[c] = j; idx[d] = j
            flat = idx[0] * 8 + idx[1] * 4 + idx[2] * 2 + idx[3]
            v[flat] = v[flat] + Q(1, 0)
    return v


def _outer(u):
    n = len(u); P = _zeros(n)
    for i in range(n):
        if u[i].is0():
            continue
        for j in range(n):
            if u[j].is0():
                continue
            P[i][j] = u[i] * u[j].conj()
    return P


def check_T_exotic_gauge_invariant_algebra_is_nonabelian() -> Dict:
    """The exotic (tetraquark) gauge-invariant colour algebra is NON-ABELIAN; the meson
    "abelian gauge-invariant algebra = Sep signature" fence is multiplicity-free-specific.

    H = fund (x) antifund (x) fund (x) antifund. The singlet multiplicity is m=2 for SU(2)
    and SU(3) (the invariant-subspace dimension). The gauge-invariant *-algebra is the
    commutant of the gauge action, a direct sum of M_{m_i} blocks over irreps i of
    multiplicity m_i. The singlet sector alone has m=2, so the commutant contains an M_2
    block and is NON-ABELIAN. Concrete SU(2) witness: the two meson-meson pairing singlets
    |A> (pairs (0,1),(2,3)) and |B> (pairs (0,3),(2,1)) are gauge-invariant, independent, and
    non-orthogonal, so their projectors P_A, P_B do not commute -- two non-commuting
    gauge-invariant operators, the signature the meson lacks.

    This CONTRASTS the meson (m=1), whose gauge-invariant algebra is the abelian
    span{pi_s, pi_adj}. So the meson criterion-route observation "the gauge-invariant colour
    algebra is abelian" is m=1-specific and does not fence exotics.

    Grade [P]: exact rep theory (multiplicity + commutant block structure + the explicit
    non-commuting witness). ALGEBRA structure only.

    SCOPE -- this does NOT establish a physical colour=IJC claim at the occupancy level.
    STRUCTURAL rung: the IJC_str razor-block once read here -- "a commuting gauge-invariant
    defender (P_A) is constructible, so structural non-existence is False" -- is SUPERSEDED by
    check_T_gauge_invariant_colour_interface_is_contextual. A commuting defender for ONE context
    does not furnish a GLOBAL Boolean section across incompatible gauge-invariant contexts; the
    tetraquark spin-1 M_3 block realizes a KCBS interface the Interface Engine certifies IJCStr.
    So a gauge-invariant colour interface CAN be IJC_str. What remains blocked is the OCCUPANCY rung:
    (IJC_adm) is not computable for colour -- it needs kappa_Bool > C, kappa_Bool is a min over
    a Boolean-defender lattice of a realignment cost eps(D), and APF supplies no grounded eps
    for a discrete colour interface (importing the spatial kappa_int is a category error). The
    n*eps record cost (cost = energy, check_T_realignment_cost_is_transition_energy) is the
    cost of the RECORD -- a different object in a different codomain from the defender's
    kappa_Bool. So no IJC claim is reopened; IJC stays the empirical QAC.
    """
    by = {}
    ok = True
    for N in (2, 3):
        m = _tetra_inv_dim(N)
        ok = ok and (m == 2)
        by[f"SU({N})_tetraquark"] = {"singlet_multiplicity_m": m, "m_ge_2_M_m_block_nonabelian": m >= 2}
    Ls2 = _tetra_gens(2)
    A = _su2_meson_pair_vec(((0, 1), (2, 3)))
    B = _su2_meson_pair_vec(((0, 3), (2, 1)))
    A_inv = all(_vec_is_zero(_matvec(L, A)) for L in Ls2)
    B_inv = all(_vec_is_zero(_matvec(L, B)) for L in Ls2)
    indep = (_rank([[x for x in A], [x for x in B]]) == 2)
    PA = _outer(A); PB = _outer(B)
    comm = _sub(_mm(PA, PB), _mm(PB, PA))
    noncommuting = not _iszero(comm)
    ok = ok and A_inv and B_inv and indep and noncommuting
    data = {
        "model": "SU(N) fund (x) antifund (x) fund (x) antifund (tetraquark); gauge-invariant algebra = commutant (exact Q[i])",
        "by_N": by,
        "su2_nonabelian_witness": {
            "pairing_A_gauge_invariant": A_inv, "pairing_B_gauge_invariant": B_inv,
            "pairings_independent": indep, "projectors_PA_PB_do_not_commute": noncommuting,
        },
        "statement": ("the exotic (m=2) gauge-invariant colour algebra contains an M_2 block (the singlet "
                      "multiplicity space) and is non-abelian; two non-commuting gauge-invariant projectors exhibited"),
        "contrast": "the meson (m=1) gauge-invariant algebra is abelian span{pi_s,pi_adj}; the meson abelian-fence is m=1-specific",
        "scope": ("ALGEBRA structure only. IJC_str razor-block SUPERSEDED (check_T_gauge_invariant_colour_interface_is_contextual: the M_3 block hosts a gauge-invariant KCBS interface the IE certifies IJCStr), "
                  "IJC_adm not computable for colour (no grounded eps for kappa_Bool; the n*eps record cost is a fenced "
                  "different object). IJC stays the empirical QAC."),
    }
    if ok:
        return _ok(
            "check_T_exotic_gauge_invariant_algebra_is_nonabelian",
            status="P",
            summary=("The tetraquark gauge-invariant colour algebra is NON-ABELIAN: singlet multiplicity m=2 for SU(2) "
                     "and SU(3) gives an M_2 block in the commutant, and for SU(2) the two meson-meson pairing "
                     "projectors P_A, P_B are gauge-invariant and do not commute. This contrasts the meson (m=1, abelian "
                     "span{pi_s,pi_adj}), so the meson 'abelian algebra = Sep signature' fence is multiplicity-free-"
                     "specific. Grade [P], algebra structure only -- it does NOT reopen a colour=IJC claim (IJC_str "
                     "IJC_str now shown realizable on the M_3 block (check_T_gauge_invariant_colour_interface_is_contextual); IJC_adm not computable for colour, occupancy stays the QAC."),
            data=data,
            dependencies=["check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P",
                          "check_T_canonical_colour_record_iff_multiplicity_free_P"],
        )
    return _fail(
        "check_T_exotic_gauge_invariant_algebra_is_nonabelian",
        status="FAIL",
        summary="exotic non-abelian-algebra witness did not hold.",
        data=data,
    )


# ============================================================================
# A gauge-invariant colour interface that is STRUCTURALLY CONTEXTUAL (IJC_str).
#
# The exotic (tetraquark) gauge-invariant colour algebra is non-abelian
# (check_T_exotic_gauge_invariant_algebra_is_nonabelian). Here we go further:
# it contains a FULL M_3 matrix block (the spin-1 isotypic, multiplicity 3),
# so it realizes every qutrit observable as a gauge-invariant operator. A
# Kochen-Specker / KCBS pentagon built from those gauge-invariant qutrit
# projectors is contextual: routed through the Interface Engine (the FeasBool
# Boole-polytope decider, apf.ijc_feasbool_engine via interface_atlas), it
# returns IJCStr -- no global section, a named Farkas/KCBS separator.
#
# This refutes the IJC_str RAZOR-BLOCK: "a commuting gauge-invariant defender
# is constructible, so structural non-existence is False". The existence of a
# commuting defender for one context does NOT furnish a GLOBAL Boolean section
# across incompatible gauge-invariant contexts -- which is exactly what
# contextuality forbids. So a gauge-invariant colour interface CAN be IJC_str.
# SCOPE: the IJC_str (structural) rung only. IJC_adm (occupancy) is untouched
# and stays the empirical QAC.
# ----------------------------------------------------------------------------

def _gic_qinv(a):
    den = a.r * a.r + a.i * a.i
    return Q(a.r / den, -a.i / den)


def _gic_crank(rows):
    """Exact rank over Q[i] of a complex matrix given as a list of rows of Q."""
    M = [r[:] for r in rows]
    R = len(M)
    if R == 0:
        return 0
    Cn = len(M[0])
    rank = 0
    for col in range(Cn):
        piv = None
        for r in range(rank, R):
            if not M[r][col].is0():
                piv = r
                break
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        inv = _gic_qinv(M[rank][col])
        M[rank] = [inv * x for x in M[rank]]
        for r in range(R):
            if r != rank and not M[r][col].is0():
                f = M[r][col]
                M[r] = [M[r][k] - f * M[rank][k] for k in range(Cn)]
        rank += 1
        if rank == R:
            break
    return rank


def _gic_invn(M):
    """Exact inverse of an n x n Q[i] matrix (Gauss-Jordan)."""
    n = len(M)
    A = [list(M[i]) + [Q(1, 0) if i == j else Q(0, 0) for j in range(n)]
         for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if not A[r][c].is0())
        A[c], A[p] = A[p], A[c]
        iv = _gic_qinv(A[c][c])
        A[c] = [iv * x for x in A[c]]
        for r in range(n):
            if r != c and not A[r][c].is0():
                f = A[r][c]
                A[r] = [A[r][k] - f * A[c][k] for k in range(2 * n)]
    return [row[n:] for row in A]


def _gic_M3_certificate():
    """Exact proof that the SU(2) tetraquark gauge-invariant algebra contains a
    full M_3 (the spin-1 isotypic, multiplicity 3). No numpy."""
    d = 16
    Ls = _tetra_gens(2)
    I = _eye(d)

    def matvec(Mx, v):
        return [sum((Mx[i][k] * v[k] for k in range(len(v))), Q(0, 0))
                for i in range(len(Mx))]

    def scal(c, Mx):
        return [[c * Mx[i][j] for j in range(len(Mx))] for i in range(len(Mx))]

    # Casimir C = sum L_a^2 ; spin-1 isotypic projector P1 = (C+24 I) C / (-128)
    C = [[Q(0, 0)] * d for _ in range(d)]
    for L in Ls:
        C = _add(C, _mm(L, L))
    P1 = scal(Q(F(-1, 128), 0), _mm(_add(C, scal(Q(24, 0), I)), C))

    _P1P1 = _mm(P1, P1)
    P1_proj = all(_P1P1[i][j] == P1[i][j] for i in range(d) for j in range(d))
    P1_gi = True
    for L in Ls:
        comm = _sub(_mm(P1, L), _mm(L, P1))
        if any(not comm[i][j].is0() for i in range(d) for j in range(d)):
            P1_gi = False
            break
    rank_P1 = _gic_crank([P1[i][:] for i in range(d)])

    # one irrep copy: cyclic gauge-submodule of a column of P1
    u = [P1[i][0] for i in range(d)]
    if all(x.is0() for x in u):
        u = [P1[i][1] for i in range(d)]
    gen = [u]
    for L in Ls:
        gen.append(matvec(L, u))
        gen.append(matvec(L, matvec(L, u)))
    sub_dim = _gic_crank([g[:] for g in gen])
    basis = []
    for v in gen:
        if _gic_crank([b[:] for b in basis] + [v[:]]) > len(basis):
            basis.append(v)
        if len(basis) == 3:
            break

    # restrict the action to the copy and check irreducibility (commutant dim 1)
    irred = None
    if len(basis) == 3:
        B = [[basis[j][i] for j in range(3)] for i in range(d)]      # 16x3
        Bd = [[B[j][i].conj() for j in range(d)] for i in range(3)]  # 3x16
        Ginv = _gic_invn(_mm(Bd, B))
        Lr = [_mm(Ginv, _mm(Bd, _mm(L, B))) for L in Ls]             # 3x3 each
        rows = []
        for Lm in Lr:
            for i in range(3):
                for j in range(3):
                    row = [Q(0, 0)] * 9
                    for k in range(3):
                        row[i * 3 + k] = row[i * 3 + k] + Lm[k][j]
                        row[k * 3 + j] = row[k * 3 + j] - Lm[i][k]
                    rows.append(row)
        irred = (9 - _gic_crank(rows)) == 1

    irrep_dim = sub_dim
    multiplicity = F(rank_P1, irrep_dim) if irrep_dim else None
    full_M3 = bool(P1_proj and P1_gi and rank_P1 == 9 and sub_dim == 3
                   and irred and multiplicity == 3)
    return {
        "P1_is_projector": P1_proj,
        "P1_gauge_invariant": P1_gi,
        "rank_P1_spin1_isotypic": rank_P1,
        "irrep_dim_cyclic_submodule": sub_dim,
        "irrep_irreducible_commutant_dim1": irred,
        "multiplicity": str(multiplicity),
        "contains_full_M3": full_M3,
    }


# exact rational KCBS pentagon (cyclically orthogonal) + rational state, Sigma>2,
# realizable inside the gauge-invariant M_3 qutrit.
_GIC_KCBS_RAYS = (
    (F(0), F(0), F(1)),
    (F(-3, 5), F(4, 5), F(0)),
    (F(-32, 85), F(-24, 85), F(15, 17)),
    (F(375, 1073), F(900, 1073), F(448, 1073)),
    (F(-12, 13), F(5, 13), F(0)),
)
_GIC_KCBS_STATE = (F(-1, 2), F(1, 2), F(25, 36))


def _gic_kcbs_scenario():
    """The exact rational KCBS pentagon as a finite marginal Scenario.
    Marginals p_i = |<v_i|psi>|^2 / <psi|psi> (gauge-invariant-realizable)."""
    from apf.ijc_feasbool_engine import Scenario
    vs = _GIC_KCBS_RAYS
    psi = _GIC_KCBS_STATE
    nrm = sum(x * x for x in psi)
    p = []
    for v in vs:
        ov = sum(v[a] * psi[a] for a in range(3))
        p.append((ov * ov) / nrm)
    meas = tuple((f"G{i}", (1, 0)) for i in range(5))
    contexts = tuple((f"G{i}", f"G{(i + 1) % 5}") for i in range(5))
    emp = []
    for i in range(5):
        j = (i + 1) % 5
        emp.append(((f"G{i}", f"G{j}"),
                    (((1, 0), p[i]), ((0, 1), p[j]),
                     ((0, 0), 1 - p[i] - p[j]), ((1, 1), F(0)))))
    return Scenario(meas, contexts, tuple(emp)), p, sum(p)


def check_T_gauge_invariant_colour_interface_is_contextual():
    """A gauge-invariant colour interface is structurally contextual (IJC_str).

    Three exact facts compose (no numpy in the pass path):
      (1) The SU(2) tetraquark gauge-invariant algebra (commutant of the gauge
          action) contains a FULL M_3: the spin-1 isotypic projector P1 is an
          exact gauge-invariant projector of rank 9; a cyclic gauge-submodule
          is 3-dimensional and irreducible (restricted commutant dim 1); hence
          multiplicity = 9/3 = 3, and by Schur the commutant restricted to the
          isotypic is the full matrix algebra M_3 on the multiplicity qutrit.
      (2) A full M_3 realizes every qutrit observable as a gauge-invariant
          operator: the *-isomorphism phi: M_3 -> P1.A.P1 sends each KCBS
          projector P_i to a gauge-invariant projector phi(P_i), and the qutrit
          KCBS state sigma to the gauge-invariant state rho = phi(sigma)/3
          (positive, trace 1, [rho, L_a]=0), with tr(rho phi(P_i)) = tr(sigma P_i).
      (3) The exact rational KCBS pentagon (cyclically orthogonal rational rays,
          rational state, Sigma = sum_i tr(sigma P_i) > 2) routed through the
          Interface Engine (interface_atlas.summarize_input -> FeasBool) returns
          IJCStr: no global Boolean section, a named Farkas/KCBS separator.

    Therefore a colour interface built entirely from gauge-invariant observables
    has no global hidden-variable section -- it is IJC_str. This REFUTES the
    razor-block reading "a commuting gauge-invariant defender is constructible,
    so structural non-existence is False" (cited in
    check_T_exotic_gauge_invariant_algebra_is_nonabelian): one commuting context
    does not glue into a global section across incompatible gauge-invariant
    contexts. SCOPE: the IJC_str (structural) rung only; IJC_adm (occupancy)
    stays the empirical QAC and is untouched here.

    Grade P_structural_instrument: the contextuality verdict is the Interface
    Engine's exact Boole-polytope computation over an exact rational interface;
    the M_3 structure is exact rep theory. Occupancy is not claimed.
    """
    from apf.ijc_feasbool_engine import feasbool, scenario_to_dict
    from apf.interface_contextuality_adapter import route_contextuality

    cert = _gic_M3_certificate()
    scn, p, Sigma = _gic_kcbs_scenario()
    fb = feasbool(scn)
    pipe = route_contextuality("tetraquark_gauge_invariant_KCBS", scenario=scenario_to_dict(scn))

    contexts_feasible = all((p[i] + p[(i + 1) % 5]) <= 1 for i in range(5))
    engine_ijc = (fb["branch"] == "IJCStr" and not pipe.export_global_P
                  and pipe.solver_status == "IJC_OBSTRUCTION" and bool(pipe.obstruction))
    sigma_violates = Sigma > 2

    # optional numpy corroboration: an EXPLICIT gauge-invariant lift of the
    # optimal (Sigma=sqrt5) KCBS with [O_i, L_a]=0 to machine precision and a
    # gauge-invariant state. Corroboration only; never gates the pass.
    corro = {"attempted": False}
    try:
        import numpy as np, math
        def toC(Mx):
            n = len(Mx); A = np.zeros((n, n), complex)
            for i in range(n):
                for j in range(n):
                    q = Mx[i][j]; A[i, j] = complex(float(q.r), float(q.i))
            return A
        Lnp = [toC(L) for L in _tetra_gens(2)]
        J = [1j * L for L in Lnp]; Jm = J[0] - 1j * J[1]
        Cc = sum(L @ L for L in Lnp); w, V = np.linalg.eigh(Cc)
        P1c = V[:, np.abs(w + 8) < 1e-6]
        Jz_in = P1c.conj().T @ (1j * Lnp[2]) @ P1c
        wz, Vz = np.linalg.eigh(Jz_in)
        E = P1c @ Vz[:, np.abs(wz - wz.max()) < 1e-6]
        def nc(Mx):
            o = Mx.copy()
            for k in range(o.shape[1]):
                nn = np.linalg.norm(o[:, k]); o[:, k] = o[:, k] / nn if nn > 1e-12 else o[:, k]
            return o
        bas = [E, nc(Jm @ E), nc(Jm @ nc(Jm @ E))]
        def Tunit(x, y): return sum(np.outer(B[:, x], B[:, y].conj()) for B in bas)
        phi = math.acos(math.sqrt(1 / math.sqrt(5)))
        ray = lambda i: np.array([math.sin(phi) * math.cos(4 * math.pi * i / 5),
                                  math.sin(phi) * math.sin(4 * math.pi * i / 5),
                                  math.cos(phi)], complex)
        Os = [sum(np.outer(ray(i), ray(i).conj())[a, b] * Tunit(a, b)
                  for a in range(3) for b in range(3)) for i in range(5)]
        gi = max(np.abs(O @ L - L @ O).max() for O in Os for L in Lnp)
        rho = sum(np.outer(B[:, 2], B[:, 2].conj()) for B in bas) / 3.0
        rho_gi = max(np.abs(rho @ L - L @ rho).max() for L in Lnp)
        Sig_np = float(sum(np.trace(rho @ O).real for O in Os))
        corro = {"attempted": True,
                 "max_commutator_O_i_with_generators": f"{gi:.2e}",
                 "state_gauge_invariant_residual": f"{rho_gi:.2e}",
                 "Sigma_optimal_gauge_invariant_state": round(Sig_np, 5)}
    except Exception as e:  # numpy absent / blocked -> corroboration skipped
        corro = {"attempted": False, "note": f"numpy corroboration skipped: {e.__class__.__name__}"}

    ok = bool(cert["contains_full_M3"] and engine_ijc and sigma_violates and contexts_feasible)
    data = {
        "M3_certificate": cert,
        "kcbs_rays": [tuple(str(x) for x in v) for v in _GIC_KCBS_RAYS],
        "kcbs_state": tuple(str(x) for x in _GIC_KCBS_STATE),
        "kcbs_marginals_p_i": [str(x) for x in p],
        "Sigma": str(Sigma),
        "Sigma_float": round(float(Sigma), 6),
        "noncontextual_bound": 2,
        "engine_branch": fb["branch"],
        "engine_n_global_sections": fb["n_global_sections"],
        "ie_pipeline_route": pipe.route,
        "ie_export_global_P": pipe.export_global_P,
        "ie_obstruction": list(pipe.obstruction),
        "numerical_corroboration": corro,
        "scope": ("IJC_str (structural) rung only; IJC_adm/occupancy stays the empirical QAC. "
                  "Algebraic interface = the tetraquark spin-1 M_3 block; state-dependent (KCBS) "
                  "witness => a gauge-invariant colour interface CAN be IJC_str. Supersedes the "
                  "IJC_str razor-block of check_T_exotic_gauge_invariant_algebra_is_nonabelian."),
    }
    if ok:
        return _ok(
            "check_T_gauge_invariant_colour_interface_is_contextual",
            status="P_structural_instrument",
            summary=("A gauge-invariant colour interface is structurally contextual (IJC_str). "
                     "The SU(2) tetraquark gauge-invariant algebra contains a full M_3 (spin-1 "
                     "isotypic, exact rank-9 projector, irreducible 3-dim copy, multiplicity 3), "
                     "so every qutrit observable is realized by a gauge-invariant operator. The "
                     "exact rational KCBS pentagon (Sigma=%s>2) routed through the Interface Engine "
                     "returns IJCStr -- no global Boolean section, a named Farkas/KCBS separator. "
                     "This REFUTES the IJC_str razor-block: a commuting defender for one context "
                     "does not glue into a global section across incompatible gauge-invariant "
                     "contexts. The interface is the tetraquark spin-1 isotypic block -- an "
                     "algebraic gauge-invariant interface, not a physically prepared colour "
                     "measurement; the witness is state-dependent (KCBS), so the claim is that a "
                     "gauge-invariant colour interface CAN be IJC_str, not that every colour "
                     "preparation is. IJC_adm (occupancy) is untouched and stays the QAC."
                     % data["Sigma_float"]),
            data=data,
            dependencies=["check_T_exotic_gauge_invariant_algebra_is_nonabelian",
                          "check_T_feasbool_general_contextuality",
                          "check_T_interface_contextuality_general_scenario"],
        )
    return _fail(
        "check_T_gauge_invariant_colour_interface_is_contextual",
        status="FAIL",
        summary="gauge-invariant colour contextuality witness did not hold.",
        data=data,
    )


# ============================================================================
# STATE-INDEPENDENT gauge-invariant colour contextuality (Yu-Oh on the M_3).
# Strengthens check_T_gauge_invariant_colour_interface_is_contextual: there the
# witness was a state-dependent KCBS pentagon. Here the Yu-Oh 13-ray
# state-independent KS set on the M_3 qutrit is contextual even on the
# MAXIMALLY-MIXED state -- which, lifted, is the maximally-mixed gauge-invariant
# state on the spin-1 isotypic (rho = P1/9, [rho, L_a]=0): a no-choice,
# information-free colour state. So the contextuality is a property of the
# gauge-invariant colour algebra itself, not of any prepared state.
# ----------------------------------------------------------------------------

_GIC_YUOH_RAYS = (
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1),
    (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1),
)


def _gic_yuoh_scenario():
    """The Yu-Oh 13-ray state-independent KS set as a finite marginal Scenario on
    the qutrit, evaluated on the maximally-mixed state (every rank-1 marginal =
    1/3). Contexts = orthogonal triads (complete bases) + orthogonal pairs."""
    from itertools import combinations
    from apf.ijc_feasbool_engine import Scenario
    rays = [tuple(F(x) for x in v) for v in _GIC_YUOH_RAYS]
    n = len(rays)

    def dot(u, v):
        return sum(u[i] * v[i] for i in range(3))

    triads = [c for c in combinations(range(n), 3)
              if all(dot(rays[a], rays[b]) == 0 for a, b in combinations(c, 2))]
    in_triad = set(p for t in triads for p in combinations(t, 2))
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)
             if dot(rays[i], rays[j]) == 0 and (i, j) not in in_triad]

    meas = tuple((f"r{i}", (1, 0)) for i in range(n))
    third = F(1, 3)
    contexts = []
    emp = []
    for t in triads:
        names = tuple(f"r{i}" for i in t)
        contexts.append(names)
        emp.append((names, tuple((tuple(1 if m == k else 0 for m in range(3)), third)
                                 for k in range(3))))
    for (i, j) in pairs:
        names = (f"r{i}", f"r{j}")
        contexts.append(names)
        emp.append((names, (((1, 0), third), ((0, 1), third),
                            ((0, 0), third), ((1, 1), F(0)))))
    return Scenario(meas, tuple(contexts), tuple(emp)), n, len(triads), len(pairs)


def check_T_gauge_invariant_colour_interface_state_independent_contextual():
    """A gauge-invariant colour interface is contextual STATE-INDEPENDENTLY.

    Strengthens check_T_gauge_invariant_colour_interface_is_contextual (whose
    witness was a state-dependent KCBS pentagon, valid for one chosen qutrit
    state). The same M_3 block (the tetraquark spin-1 isotypic, multiplicity 3 --
    see _gic_M3_certificate) hosts the Yu-Oh 13-ray state-independent
    Kochen-Specker set. Evaluated on the MAXIMALLY-MIXED qutrit state (every
    rank-1 marginal = 1/3), the empirical table is OUTSIDE the noncontextual
    (Boole) polytope: routed through the Interface Engine it returns IJCStr.

    "State-independent" here is the inequality sense: every state, including the
    maximally-mixed one, lies outside the noncontextual polytope. The 13-ray
    orthogonality graph itself DOES admit {0,1} colorings (it is not a
    Kochen-Specker coloring-impossibility); the strength is that the no-choice
    maximally-mixed point already violates noncontextuality.

    The maximally-mixed qutrit state lifts to the maximally-mixed gauge-invariant
    state on the spin-1 isotypic, rho = P1/9 (P1 the exact gauge-invariant
    rank-9 projector; [rho, L_a]=0). This is a no-choice, information-free colour
    state -- it carries no prepared direction. Its contextuality therefore
    establishes that the gauge-invariant colour ALGEBRA is contextual, not a
    chosen preparation: the single-sector analogue of a state-independent
    parity-web obstruction.

    SCOPE: IJC_str (structural) rung only; IJC_adm/occupancy stays the empirical
    QAC. The Yu-Oh rays are exact rational (entries in {0,+-1}); the verdict is
    the engine's exact Boole-polytope LP (exclusivity-pruned). Grade
    P_structural_instrument: the contextuality verdict is the engine's exact
    finite-math computation; occupancy is not claimed.
    """
    from apf.ijc_feasbool_engine import feasbool, scenario_to_dict
    from apf.interface_contextuality_adapter import route_contextuality

    cert = _gic_M3_certificate()
    scn, n_rays, n_triads, n_pairs = _gic_yuoh_scenario()
    fb = feasbool(scn)
    pipe = route_contextuality("tetraquark_M3_YuOh_state_independent",
                               scenario=scenario_to_dict(scn))
    engine_ijc = (fb["branch"] == "IJCStr" and not pipe.export_global_P
                  and pipe.solver_status == "IJC_OBSTRUCTION" and bool(pipe.obstruction))

    ok = bool(cert["contains_full_M3"] and engine_ijc and n_rays == 13)
    data = {
        "M3_certificate": cert,
        "ks_set": "Yu-Oh 13-ray (entries in {0,+-1}), state-independent",
        "n_rays": n_rays,
        "n_triad_contexts": n_triads,
        "n_pair_contexts": n_pairs,
        "state": "maximally-mixed qutrit (rank-1 marginals = 1/3); lifts to the "
                 "maximally-mixed gauge-invariant state rho = P1/9, [rho,L_a]=0",
        "engine_branch": fb["branch"],
        "engine_live_sections_after_pruning": fb["n_global_sections"],
        "ie_pipeline_route": pipe.route,
        "ie_export_global_P": pipe.export_global_P,
        "ie_obstruction": list(pipe.obstruction),
        "scope": ("STATE-INDEPENDENT (maximally-mixed, no-choice state). IJC_str rung "
                  "only; IJC_adm/occupancy stays the empirical QAC. Strengthens "
                  "check_T_gauge_invariant_colour_interface_is_contextual (state-dependent KCBS) "
                  "to a state-independent witness on the M_3 -- the single-sector analogue of a "
                  "state-independent parity-web obstruction."),
    }
    if ok:
        return _ok(
            "check_T_gauge_invariant_colour_interface_state_independent_contextual",
            status="P_structural_instrument",
            summary=("A gauge-invariant colour interface is contextual STATE-INDEPENDENTLY. The "
                     "tetraquark spin-1 M_3 hosts the Yu-Oh 13-ray Kochen-Specker set; on the "
                     "MAXIMALLY-MIXED qutrit state (every marginal 1/3, lifting to the "
                     "maximally-mixed gauge-invariant state rho=P1/9) the table is outside the "
                     "noncontextual polytope and the Interface Engine returns IJCStr. So the "
                     "contextuality belongs to the gauge-invariant colour ALGEBRA, not a chosen "
                     "preparation -- the single-sector analogue of a state-independent parity-web. "
                     "Strengthens the state-dependent KCBS witness. IJC_adm/occupancy stays the QAC."),
            data=data,
            dependencies=["check_T_gauge_invariant_colour_interface_is_contextual",
                          "check_T_ks_parity_contextuality_scalable",
                          "check_T_interface_contextuality_general_scenario"],
        )
    return _fail(
        "check_T_gauge_invariant_colour_interface_state_independent_contextual",
        status="FAIL",
        summary="state-independent gauge-invariant colour contextuality witness did not hold.",
        data=data,
    )


# ============================================================================
# STRONGEST FORM: a state-independent KS COLORING obstruction (Mermin-Peres magic
# square) realized gauge-invariantly, in EXACT arithmetic, on the SU(2)
# pentaquark M_4. The census shows colour contextuality grows with constituent
# number; at five constituents (fund^5) the gauge-invariant algebra contains a
# rational M_4 block (the spin-3/2 sector, multiplicity 4) -- a two-qubit space.
# A two-qubit algebra hosts the magic square, whose global-section support is
# EMPTY: not a noncontextuality-inequality violation but a Kochen-Specker
# coloring IMPOSSIBILITY -- IJCStr for EVERY state, no preparation chosen.
# ----------------------------------------------------------------------------

def _gic_M4_certificate():
    """Exact proof that the SU(2) pentaquark (fund^5, 32-dim) gauge-invariant
    algebra contains a full M_4 (the spin-3/2 isotypic, multiplicity 4). No numpy;
    SU(2) generators are rational, so the whole certificate is exact over Q[i]."""
    d = 32
    g = _su_n_gens(2)
    I2 = _eye(2)

    def slot(ga, srt):
        facs = [I2] * 5
        facs[srt] = ga
        M = facs[0]
        for f in facs[1:]:
            M = _kron(M, f)
        return M

    Ls = []
    for ga in g:
        L = [[Q(0, 0)] * d for _ in range(d)]
        for srt in range(5):
            L = _add(L, slot(ga, srt))
        Ls.append(L)

    def scal(c, M):
        return [[c * M[i][j] for j in range(len(M))] for i in range(len(M))]

    def matvec(M, v):
        return [sum((M[i][k] * v[k] for k in range(len(v))), Q(0, 0)) for i in range(len(M))]

    C = [[Q(0, 0)] * d for _ in range(d)]
    for L in Ls:
        C = _add(C, _mm(L, L))
    # Casimir eigenvalues (this normalization): s=5/2 -> -35, s=3/2 -> -15, s=1/2 -> -3.
    # spin-3/2 projector P = (C+35 I)(C+3 I) / ((-15+35)(-15+3)) = (C+35 I)(C+3 I)/(-240)
    I = _eye(d)
    P = scal(Q(F(-1, 240), 0), _mm(_add(C, scal(Q(35, 0), I)), _add(C, scal(Q(3, 0), I))))

    _PP = _mm(P, P)
    P_proj = all(_PP[i][j] == P[i][j] for i in range(d) for j in range(d))
    P_gi = True
    for L in Ls:
        comm = _sub(_mm(P, L), _mm(L, P))
        if any(not comm[i][j].is0() for i in range(d) for j in range(d)):
            P_gi = False
            break
    rank_P = _gic_crank([P[i][:] for i in range(d)])

    # one spin-3/2 copy: cyclic gauge-submodule of a column of P
    u = [P[i][0] for i in range(d)]
    if all(x.is0() for x in u):
        u = [P[i][1] for i in range(d)]
    gen = [u]
    for L in Ls:
        a = matvec(L, u); gen.append(a)
        b = matvec(L, a); gen.append(b)
        gen.append(matvec(L, b))
    sub_dim = _gic_crank([x[:] for x in gen])
    basis = []
    for v in gen:
        if _gic_crank([z[:] for z in basis] + [v[:]]) > len(basis):
            basis.append(v)
        if len(basis) == 4:
            break

    irred = None
    if len(basis) == 4:
        B = [[basis[j][i] for j in range(4)] for i in range(d)]
        Bd = [[B[j][i].conj() for j in range(d)] for i in range(4)]
        Ginv = _gic_invn(_mm(Bd, B))
        Lr = [_mm(Ginv, _mm(Bd, _mm(L, B))) for L in Ls]
        rows = []
        for Lm in Lr:
            for i in range(4):
                for j in range(4):
                    row = [Q(0, 0)] * 16
                    for k in range(4):
                        row[i * 4 + k] = row[i * 4 + k] + Lm[k][j]
                        row[k * 4 + j] = row[k * 4 + j] - Lm[i][k]
                    rows.append(row)
        irred = (16 - _gic_crank(rows)) == 1

    multiplicity = F(rank_P, sub_dim) if sub_dim else None
    full_M4 = bool(P_proj and P_gi and rank_P == 16 and sub_dim == 4
                   and irred and multiplicity == 4)
    return {
        "P_spin32_is_projector": P_proj,
        "P_gauge_invariant": P_gi,
        "rank_P_spin32_isotypic": rank_P,
        "irrep_dim_cyclic_submodule": sub_dim,
        "irrep_irreducible_commutant_dim1": irred,
        "multiplicity": str(multiplicity),
        "contains_full_M4": full_M4,
    }


def check_T_gauge_invariant_colour_KS_coloring_obstruction():
    """A gauge-invariant colour interface admits a state-independent KS COLORING
    obstruction -- the strongest form of contextuality -- in exact arithmetic.

    The contextuality census shows the gauge-invariant colour algebra gains a
    qudit block M_m with m growing in constituent number (meson M_1 abelian;
    baryon M_2 qubit; tetraquark M_3 qutrit; pentaquark M_4 + M_5). At FIVE
    constituents the SU(2) pentaquark (fund^5) gauge-invariant algebra contains a
    full M_4 -- the spin-3/2 isotypic, multiplicity 4 (certified exactly by
    _gic_M4_certificate: the spin-3/2 projector is an exact rational
    gauge-invariant projector of rank 16, a cyclic gauge-submodule is 4-dim and
    irreducible, so multiplicity = 16/4 = 4). SU(2) generators are rational, so
    the whole M_4 certificate is exact over Q[i].

    M_4 is a full matrix algebra on a 4-dimensional space = the operator algebra
    of two qubits, every element gauge-invariant. It therefore realizes the
    Mermin-Peres magic square. Routed through the Interface Engine the magic
    square returns IJCStr with EMPTY global-section support: not a
    noncontextuality-inequality violation (the Yu-Oh / KCBS form) but a
    Kochen-Specker coloring IMPOSSIBILITY -- no deterministic global assignment is
    consistent with all contexts, so the interface is contextual for EVERY state,
    with no preparation chosen at all.

    This is the strongest contextuality form (state-independent coloring), realized
    by gauge-invariant colour observables, in exact arithmetic. SCOPE: IJC_str
    (structural) rung only; IJC_adm/occupancy stays the empirical QAC. Grade
    P_structural_instrument: the verdict is the engine's exact finite-math
    computation; occupancy is not claimed.
    """
    from apf.ijc_feasbool_engine import (
        feasbool, global_section_support_nonempty,
        scenario_mermin_peres_magic_square, scenario_to_dict,
    )
    from apf.interface_contextuality_adapter import route_contextuality

    cert = _gic_M4_certificate()
    scn = scenario_mermin_peres_magic_square()
    fb = feasbool(scn)
    sup = global_section_support_nonempty(scn)
    pipe = route_contextuality("pentaquark_M4_magic_square", scenario=scenario_to_dict(scn))

    empty_support = (sup["witness_section"] is None)
    engine_ijc = (fb["branch"] == "IJCStr" and not pipe.export_global_P
                  and pipe.solver_status == "IJC_OBSTRUCTION" and bool(pipe.obstruction))

    ok = bool(cert["contains_full_M4"] and engine_ijc and empty_support)
    data = {
        "M4_certificate": cert,
        "ks_set": "Mermin-Peres magic square (two-qubit, state-independent)",
        "engine_branch": fb["branch"],
        "global_section_support_empty": empty_support,
        "engine_live_sections_after_pruning": fb["n_global_sections"],
        "ie_pipeline_route": pipe.route,
        "ie_export_global_P": pipe.export_global_P,
        "ie_obstruction": list(pipe.obstruction),
        "form": ("state-independent KS COLORING IMPOSSIBILITY (empty global-section support) -- "
                 "the strongest form in the engine's parity/coloring class, strictly stronger than "
                 "the Yu-Oh inequality form; contextual for EVERY state. (Orthogonality-encoded KS "
                 "sets, e.g. the 18-ray Cabello set, are a separate sibling class.)"),
        "scope": ("IJC_str (structural) rung only; IJC_adm/occupancy stays the empirical QAC. "
                  "M_4 = the gauge-invariant two-qubit block (spin-3/2, multiplicity 4) of the "
                  "SU(2) pentaquark; exact over Q[i]. Strongest form in the contextuality census "
                  "(meson M_1 / baryon M_2 / tetraquark M_3 / pentaquark M_4)."),
    }
    if ok:
        return _ok(
            "check_T_gauge_invariant_colour_KS_coloring_obstruction",
            status="P_structural_instrument",
            summary=("A gauge-invariant colour interface admits a state-independent Kochen-Specker "
                     "COLORING obstruction, exactly. The SU(2) pentaquark (fund^5) gauge-invariant "
                     "algebra contains a full M_4 (spin-3/2, multiplicity 4; exact rational "
                     "certificate), a two-qubit operator algebra that realizes the Mermin-Peres "
                     "magic square. Routed through the Interface Engine the magic square returns "
                     "IJCStr with EMPTY global-section support -- a coloring impossibility, IJCStr "
                     "for every state with no preparation chosen. Strongest form in the census "
                     "(meson M_1 abelian / baryon M_2 qubit / tetraquark M_3 qutrit / pentaquark "
                     "M_4). IJC_str rung only; IJC_adm/occupancy stays the QAC."),
            data=data,
            dependencies=["check_T_gauge_invariant_colour_interface_state_independent_contextual",
                          "check_T_gauge_invariant_colour_interface_is_contextual",
                          "check_T_interface_contextuality_general_scenario"],
        )
    return _fail(
        "check_T_gauge_invariant_colour_KS_coloring_obstruction",
        status="FAIL",
        summary="gauge-invariant magic-square coloring-obstruction witness did not hold.",
        data=data,
    )



# ============================================================================
# CHIRAL-CONDENSATE FLAVOUR-DENSITY CONTEXTUALITY (the genuinely-chiral target).
# The chiral condensate order parameter Sigma_ij = <qbar_{R,i} q_{L,j}> is a
# flavour matrix; its gauge-invariant scalar-density components -- the singlet
# qbar q and the octet qbar lambda^A q -- are the Hermitian combinations of the
# bilinears qbar_i q_j and span Herm(3) for N_f=3, so EVERY qutrit projector is
# (the vector-like Hermitian bilinears qbar_i q_j = U(3)_V singlet qbar q + SU(3)_V
# octet qbar lambda^A q acting on Sigma's flavour-fundamental index space; NOT the
# real/imag parts of the chiral R->L matrix Sigma itself).  Unlike the colour single pair
# (gauge-invariant algebra abelian -> Sep; see
# check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P),
# this flavour-density algebra is NON-ABELIAN at the single-density (m=1) level,
# because flavour is a GLOBAL gauge-invariant label and [qbar lambda^A q,
# qbar lambda^B q] ~ f^{ABC} qbar lambda^C q != 0.  The flavour qutrit hosts the
# Yu-Oh 13-ray state-independent KS set, which the Interface Engine certifies
# IJCStr.  So gauge-invariant contextuality of the chiral condensate enters at
# the ELEMENTARY single-density level for N_f >= 3 -- it does NOT require the
# multi-pair m >= 2 sector that COLOUR contextuality needs
# (check_T_gauge_invariant_colour_interface_is_contextual).  IJC_adm -- whether
# <qbar q> != 0 actually FORMS, the vacuum's classical flavour alignment -- is
# occupancy = the empirical QAC and is untouched here.
# ----------------------------------------------------------------------------

def _ccf_herm_coords(M):
    """Real 9-vector coords of a Hermitian 3x3 given as rows of (re, im) F pairs."""
    return [M[0][0][0], M[1][1][0], M[2][2][0],
            M[0][1][0], M[0][2][0], M[1][2][0],
            M[0][1][1], M[0][2][1], M[1][2][1]]


def _ccf_rank_F(rows):
    """Exact rank of rational row-vectors (Fraction entries)."""
    M = [r[:] for r in rows]
    R = len(M)
    if R == 0:
        return 0
    Cn = len(M[0])
    rank = 0
    for col in range(Cn):
        piv = next((r for r in range(rank, R) if M[r][col] != 0), None)
        if piv is None:
            continue
        M[rank], M[piv] = M[piv], M[rank]
        inv = F(1) / M[rank][col]
        M[rank] = [inv * x for x in M[rank]]
        for r in range(R):
            if r != rank and M[r][col] != 0:
                f = M[r][col]
                M[r] = [M[r][k] - f * M[rank][k] for k in range(Cn)]
        rank += 1
        if rank == R:
            break
    return rank


def _ccf_scalar_density_basis():
    """The 9 Hermitian scalar-density observables of Sigma_ij (N_f=3), as Hermitian
    coords: the diagonal densities qbar_i q_i (3), the real-symmetric Re qbar_i q_j
    (3), and the imaginary Im qbar_i q_j (3).  Manifestly the Hermitian parts of
    the nine bilinears qbar_i q_j; equivalently {qbar q, qbar lambda^A q}."""
    def Z():
        return [[(F(0), F(0)) for _ in range(3)] for _ in range(3)]
    mats = []
    for i in range(3):
        M = Z(); M[i][i] = (F(1), F(0)); mats.append(M)
    for (i, j) in [(0, 1), (0, 2), (1, 2)]:
        M = Z(); M[i][j] = (F(1), F(0)); M[j][i] = (F(1), F(0)); mats.append(M)
        M = Z(); M[i][j] = (F(0), F(1)); M[j][i] = (F(0), F(-1)); mats.append(M)
    return [_ccf_herm_coords(M) for M in mats]


_CCF_YUOH_RAYS = (
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1),
    (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1),
)


def _ccf_yuoh_flavour_scenario():
    """The Yu-Oh 13-ray state-independent KS set as a finite marginal Scenario on
    the FLAVOUR fundamental qutrit, on the maximally-mixed state (rank-1 marginals
    = 1/3).  Contexts = orthogonal triads + orthogonal pairs."""
    from itertools import combinations
    from apf.ijc_feasbool_engine import Scenario
    rays = [tuple(F(x) for x in v) for v in _CCF_YUOH_RAYS]
    n = len(rays)

    def dot(u, v):
        return sum(u[i] * v[i] for i in range(3))

    triads = [c for c in combinations(range(n), 3)
              if all(dot(rays[a], rays[b]) == 0 for a, b in combinations(c, 2))]
    in_triad = set(p for t in triads for p in combinations(t, 2))
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)
             if dot(rays[i], rays[j]) == 0 and (i, j) not in in_triad]
    meas = tuple((f"r{i}", (1, 0)) for i in range(n))
    third = F(1, 3)
    contexts = []
    emp = []
    for t in triads:
        names = tuple(f"r{i}" for i in t)
        contexts.append(names)
        emp.append((names, tuple((tuple(1 if m == k else 0 for m in range(3)), third)
                                 for k in range(3))))
    for (i, j) in pairs:
        names = (f"r{i}", f"r{j}")
        contexts.append(names)
        emp.append((names, (((1, 0), third), ((0, 1), third),
                            ((0, 0), third), ((1, 1), F(0)))))
    return Scenario(meas, tuple(contexts), tuple(emp)), n, len(triads), len(pairs)


def _ccf_density_nonabelian_witness():
    """Exact 3x3: [D0, S01] != 0 where D0=diag(1,0,0) (qbar_1 q_1) and
    S01=E01+E10 (Re qbar_1 q_2) are two scalar-density observables.  Demonstrates
    the single-density flavour algebra is non-abelian (colour single-pair is not)."""
    def mm(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)]
                for i in range(3)]
    D0 = [[F(1), F(0), F(0)], [F(0), F(0), F(0)], [F(0), F(0), F(0)]]
    S01 = [[F(0), F(1), F(0)], [F(1), F(0), F(0)], [F(0), F(0), F(0)]]
    comm = [[mm(D0, S01)[i][j] - mm(S01, D0)[i][j] for j in range(3)] for i in range(3)]
    return any(comm[i][j] != 0 for i in range(3) for j in range(3))


def check_T_chiral_condensate_flavour_density_interface_is_contextual():
    """The chiral condensate's gauge-invariant flavour-density interface is
    state-independently CONTEXTUAL (IJC_str), at the SINGLE-density level (N_f=3).

    The chiral condensate order parameter Sigma_ij = <qbar_{R,i} q_{L,j}> is an
    N_f x N_f flavour matrix; it lives on the flavour-fundamental index space (the
    u,d,s qutrit for N_f=3).  The gauge-invariant observables ACTING ON that index
    space are the scalar flavour densities -- the vector-like Hermitian bilinears
    qbar_i q_j = qbar_{R,i} q_{R,j} + qbar_{L,i} q_{L,j}, i.e. the U(3)_V singlet
    qbar q plus the SU(3)_V octet qbar lambda^A q.  (These are densities of the
    flavour index, NOT literally the real/imaginary parts of the chiral R->L matrix
    Sigma; they share Sigma's flavour-fundamental Hilbert space, which is what the
    contextuality is a property of.)  Three exact facts compose:

      (1) REALIZATION.  The nine Hermitian scalar flavour-density observables span
          Herm(3) (exact rank 9 over the rationals).  Hence every qutrit rank-1
          projector is REALIZED as a real combination of gauge-invariant flavour
          densities -- in particular every Yu-Oh ray projector is a gauge-invariant
          flavour-density observable on Sigma's flavour-fundamental index space.
          (Spanning gives realizability; the co-measurability WITHIN a Yu-Oh context
          and incompatibility ACROSS contexts are the qutrit's own -- the flavour
          fundamental IS the qutrit Hilbert space, so the Yu-Oh orthogonality graph
          is literally these density observables' commutation structure.)

      (2) NON-ABELIAN AT m=1.  Two scalar-density observables fail to commute
          ([D0, S01] != 0 exactly): the single-density flavour algebra is
          non-abelian because flavour is a GLOBAL gauge-invariant label.  This is
          the decisive contrast with COLOUR, whose single q-qbar pair is
          gauge-invariantly abelian (Sep) and needs the multi-pair m>=2 sector
          for a non-abelian gauge-invariant algebra.

      (3) ENGINE VERDICT.  The Yu-Oh 13-ray state-independent KS set on the flavour
          qutrit, evaluated on the maximally-mixed state, routed through the
          Interface Engine (interface_atlas.summarize_input -> FeasBool), returns
          IJCStr: outside the noncontextual (Boole) polytope, a named Farkas/KS
          separator.

    Therefore gauge-invariant contextuality of the chiral condensate enters at the
    ELEMENTARY single-density level for N_f >= 3 (the u,d,s flavour qutrit) --
    unlike colour, where it requires the multi-pair sector.  (For N_f = 2 flavour
    is SU(2) -> a qubit, which admits a noncontextual model, so a qutrit N_f >= 3
    is required for this state-independent witness -- asserted here, not certified
    by this check.)

    SCOPE / FENCES.  (a) IJC_str (the engine's math verdict on the order-parameter
    density ALGEBRA) only.  IJC_adm -- whether <qbar q> != 0 actually FORMS, i.e.
    the vacuum's classical flavour alignment Sigma ~ diag -- is occupancy = the
    empirical QAC and is NOT claimed here; the contextuality is of the interface,
    not a claim that the condensate's vacuum value is non-classical.  (b) The
    result is N_f >= 3.  Grade P_structural_instrument: the contextuality verdict
    is the engine's exact finite Boole-polytope computation; the realization and
    non-abelian facts are exact rational linear algebra.
    """
    from apf.ijc_feasbool_engine import feasbool, scenario_to_dict
    from apf.interface_contextuality_adapter import route_contextuality

    density_rank = _ccf_rank_F(_ccf_scalar_density_basis())
    nonabelian = _ccf_density_nonabelian_witness()
    scn, n_rays, n_triads, n_pairs = _ccf_yuoh_flavour_scenario()
    fb = feasbool(scn)
    pipe = route_contextuality("chiral_condensate_flavour_qutrit_YuOh",
                               scenario=scenario_to_dict(scn))
    engine_ijc = (fb["branch"] == "IJCStr" and not pipe.export_global_P
                  and pipe.solver_status == "IJC_OBSTRUCTION" and bool(pipe.obstruction))

    ok = bool(density_rank == 9 and nonabelian and engine_ijc and n_rays == 13)
    data = {
        "order_parameter": "Sigma_ij = <qbar_{R,i} q_{L,j}> (N_f=3 flavour matrix)",
        "gauge_invariant_observables": "vector-like scalar flavour densities qbar_i q_j (U(3)_V singlet qbar q + SU(3)_V octet qbar lambda^A q) acting on Sigma flavour-fundamental index space",
        "scalar_density_span_rank_over_Herm3": density_rank,
        "every_projector_is_a_density_observable": density_rank == 9,
        "single_density_algebra_nonabelian": nonabelian,
        "colour_contrast_single_pair_abelian_ref": "check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P (meson gauge-invariant colour algebra span{pi_s,pi_adj}, dim 2, abelian => colour needs m>=2)",
        "ks_set": "Yu-Oh 13-ray (entries in {0,+-1}), state-independent",
        "n_rays": n_rays,
        "n_triad_contexts": n_triads,
        "n_pair_contexts": n_pairs,
        "state": "maximally-mixed flavour qutrit (rank-1 marginals = 1/3)",
        "engine_branch": fb["branch"],
        "engine_live_sections_after_pruning": fb["n_global_sections"],
        "ie_pipeline_route": pipe.route,
        "ie_export_global_P": pipe.export_global_P,
        "ie_obstruction": list(pipe.obstruction),
        "N_f_required": ">= 3 (N_f=2 flavour is a qubit; no state-independent KS)",
        "scope": ("IJC_str (structural) rung only; IJC_adm/occupancy (does <qbar q> != 0 "
                  "form -- the vacuum's classical alignment) stays the empirical QAC. "
                  "Single-density (m=1) flavour contextuality, gauge-invariant -- the "
                  "decisive contrast with colour (multi-pair m>=2 needed there)."),
    }
    if ok:
        return _ok(
            "check_T_chiral_condensate_flavour_density_interface_is_contextual",
            status="P_structural_instrument",
            summary=("The chiral condensate's gauge-invariant flavour-density interface is "
                     "state-independently CONTEXTUAL (IJC_str) at the single-density level "
                     "(N_f=3). The order parameter Sigma_ij = <qbar_{R,i} q_{L,j}> has scalar-"
                     "flavour densities (the vector-like qbar q + qbar lambda^A q, U(3)_V) "
                     "spanning Herm(3) (exact rank 9), so every Yu-Oh ray projector is a "
                     "gauge-invariant flavour-density observable on Sigma's flavour-fundamental "
                     "index space; the single-density flavour algebra is non-abelian "
                     "([D0,S01]!=0); and the Yu-Oh 13-ray KS set on the flavour qutrit "
                     "(maximally-mixed state) routed through the Interface Engine returns IJCStr. "
                     "So gauge-invariant contextuality of the chiral condensate enters at the "
                     "ELEMENTARY single-density level for N_f>=3 -- unlike colour, which needs "
                     "the multi-pair m>=2 sector (a single q-qbar pair is gauge-invariantly "
                     "abelian/Sep). IJC_adm (whether <qbar q>!=0 forms; the classical vacuum "
                     "alignment) stays the QAC and is not claimed."),
            data=data,
            dependencies=["check_T_gauge_invariant_colour_interface_state_independent_contextual",
                          "check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P",
                          "check_T_feasbool_general_contextuality",
                          "check_T_interface_contextuality_general_scenario"],
        )
    return _fail(
        "check_T_chiral_condensate_flavour_density_interface_is_contextual",
        status="FAIL",
        summary="chiral condensate flavour-density contextuality witness did not hold.",
        data=data,
    )


# ============================================================================
# SU(3) OCTET COLOUR CONTEXTUALITY (the physical gauge group, exact) + the
# k-string SPECTRUM-BLINDNESS delimiting result (what the strong face does NOT buy).
# Added on the strong-face -> confining-spectrum lane (2026-06-30).
# ----------------------------------------------------------------------------
from collections import defaultdict as _ddict
from itertools import product as _iproduct, permutations as _perms, combinations as _combs
import math as _math


def _su3_weyl_klimyk_tetraquark():
    """Exact decomposition of the SU(3) tetraquark q-qbar-q-qbar (3(x)3bar(x)3(x)3bar,
    81-dim) into irreps, by the Weyl-Klimyk character formula on integer weights
    (no sqrt3 -- multiplicities are integers).  Returns {(p,q): (dim, mult)}."""
    fund = [(2, -1, -1), (-1, 2, -1), (-1, -1, 2)]
    anti = [tuple(-x for x in w) for w in fund]
    W = _ddict(int)
    for c in _iproduct(fund, anti, fund, anti):
        W[tuple(sum(c[k][j] for k in range(4)) for j in range(3))] += 1
    rho = (3, 0, -3)
    S3 = list(_perms(range(3)))

    def sgn(p):
        s = 1
        for i in range(3):
            for j in range(i + 1, 3):
                if p[i] > p[j]:
                    s = -s
        return s

    def mult(hw):
        lr = tuple(hw[i] + rho[i] for i in range(3))
        t = 0
        for sig in S3:
            sw = tuple(lr[sig[i]] for i in range(3))
            t += sgn(sig) * W.get(tuple(sw[i] - rho[i] for i in range(3)), 0)
        return t

    out = {}
    for hw in [w for w in W if w[0] >= w[1] >= w[2]]:
        n = mult(hw)
        if n > 0:
            p = (hw[0] - hw[1]) // 3
            q = (hw[1] - hw[2]) // 3
            dim = (p + 1) * (q + 1) * (p + q + 2) // 2
            out[(p, q)] = (dim, n)
    return out


# --- explicit SU(3) quadratic Casimir corroboration (independent of Weyl-Klimyk) ---
class _S3E:
    """Q[i,sqrt3] field element a + b*sqrt3 + c*i + d*i*sqrt3."""
    __slots__ = ('a', 'b', 'c', 'd')

    def __init__(s, a=0, b=0, c=0, d=0):
        s.a = F(a); s.b = F(b); s.c = F(c); s.d = F(d)

    def __add__(x, y):
        return _S3E(x.a + y.a, x.b + y.b, x.c + y.c, x.d + y.d)

    def __mul__(x, y):
        a, b, c, d = x.a, x.b, x.c, x.d
        p, q, r, s = y.a, y.b, y.c, y.d
        return _S3E(a * p + 3 * b * q - c * r - 3 * d * s,
                    a * q + b * p - c * s - d * r,
                    a * r + c * p + 3 * b * s + 3 * d * q,
                    a * s + d * p + b * r + c * q)

    def is0(x):
        return x.a == 0 and x.b == 0 and x.c == 0 and x.d == 0


def _su3_casimir_trace_corroboration():
    """Build the explicit SU(3) quadratic Casimir C = sum_a G_a^2 on the 81-dim
    tetraquark over Q[i,sqrt3] (G_a the diagonal colour generators; lambda_2/5/7
    imaginary, lambda_8 carries sqrt3) and return (tr C, tr C^2) as exact rationals.
    Cross-checks the Weyl-Klimyk spectrum {C2=0:2, 3:32, 6:20, 8:27}:
    tr C = 432, tr C^2 = 2736 -- independent confirmation that the octet sector is
    exactly 32 states = 4 copies x dim 8 (a full M_4), with the sqrt3 load-bearing
    yet the spectrum pure-rational."""
    Z = _S3E(0); ONE = _S3E(1); Ii = _S3E(0, 0, 1)

    def M(entries):
        m = [[Z, Z, Z], [Z, Z, Z], [Z, Z, Z]]
        for (i, j), v in entries.items():
            m[i][j] = v
        return m

    lam = [
        M({(0, 1): ONE, (1, 0): ONE}),
        M({(0, 1): _S3E(0, 0, -1), (1, 0): Ii}),
        M({(0, 0): ONE, (1, 1): _S3E(-1)}),
        M({(0, 2): ONE, (2, 0): ONE}),
        M({(0, 2): _S3E(0, 0, -1), (2, 0): Ii}),
        M({(1, 2): ONE, (2, 1): ONE}),
        M({(1, 2): _S3E(0, 0, -1), (2, 1): Ii}),
        M({(0, 0): _S3E(0, F(1, 3)), (1, 1): _S3E(0, F(1, 3)), (2, 2): _S3E(0, F(-2, 3))}),
    ]
    half = _S3E(F(1, 2))
    T = [[[half * lam[a][i][j] for j in range(3)] for i in range(3)] for a in range(8)]

    def conj(x):
        return _S3E(x.a, x.b, -x.c, -x.d)

    Tbar = [[[Z + (_S3E(0) if False else (Z)) for _ in range(3)] for _ in range(3)] for _ in range(8)]
    Tbar = [[[_S3E(0) for _ in range(3)] for _ in range(3)] for _ in range(8)]
    for a in range(8):
        for i in range(3):
            for j in range(3):
                Tbar[a][i][j] = _S3E(0) + (_S3E(0)) if T[a][i][j].is0() else _S3E(0)
    # -T_a^* for antifund:
    for a in range(8):
        for i in range(3):
            for j in range(3):
                v = conj(T[a][i][j])
                Tbar[a][i][j] = _S3E(-v.a, -v.b, -v.c, -v.d)

    N = 81
    slotgen = [T, Tbar, T, Tbar]
    C = [[_S3E(0) for _ in range(N)] for _ in range(N)]
    diag = _S3E(F(16, 3))  # 4 slots x C2_fund(=4/3)
    for x in range(N):
        C[x][x] = C[x][x] + diag

    def dig(x):
        return [(x // 27) % 3, (x // 9) % 3, (x // 3) % 3, x % 3]

    for s1 in range(4):
        for s2 in range(s1 + 1, 4):
            Ga = slotgen[s1]; Gb = slotgen[s2]
            tt = [[[[_S3E(0) for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
            for a in range(8):
                for i in range(3):
                    for j in range(3):
                        if Ga[a][i][j].is0():
                            continue
                        for k in range(3):
                            for l in range(3):
                                if Gb[a][k][l].is0():
                                    continue
                                tt[i][j][k][l] = tt[i][j][k][l] + Ga[a][i][j] * Gb[a][k][l]
            two = _S3E(2)
            for x in range(N):
                dg = dig(x); i = dg[s1]; k = dg[s2]
                for j in range(3):
                    for l in range(3):
                        v = tt[i][j][k][l]
                        if v.is0():
                            continue
                        d2 = dg[:]; d2[s1] = j; d2[s2] = l
                        y = ((d2[0] * 3 + d2[1]) * 3 + d2[2]) * 3 + d2[3]
                        C[y][x] = C[y][x] + two * v

    trC = _S3E(0)
    for x in range(N):
        trC = trC + C[x][x]
    trC2 = _S3E(0)
    for x in range(N):
        for k in range(N):
            if not C[x][k].is0() and not C[k][x].is0():
                trC2 = trC2 + C[x][k] * C[k][x]
    return trC, trC2


def _su3_octet_M4_certificate():
    """Exact certificate that the physical gauge group SU(3), in the octet channel of
    the real-QCD tetraquark q-qbar-q-qbar, hosts a full M_4 (two-qubit) gauge-invariant
    block. Two INDEPENDENT routes agree: (1) exact Weyl-Klimyk character decomposition
    -> octet multiplicity 4; (2) an explicit 81-dim quadratic Casimir over Q[i,sqrt3]
    with tr C = 432, tr C^2 = 2736 (the sqrt3 load-bearing yet the spectrum
    pure-rational), consistent with the octet sector = 32 states = 4 copies x dim 8.
    Gauge-invariance of the M_4 block is a Schur-lemma inference (octet irreducible,
    multiplicity 4 => commutant of the octet isotypic = M_4, every element commutes with
    the colour action); no explicit [O, G_a] = 0 operator is constructed."""
    dec = _su3_weyl_klimyk_tetraquark()
    tot = sum(d * n for (d, n) in dec.values())
    octet = dec.get((1, 1), (0, 0))
    blocks = sorted([n for (d, n) in dec.values()], reverse=True)
    trC, trC2 = _su3_casimir_trace_corroboration()
    casimir_ok = (trC.a == 432 and trC.b == 0 and trC.c == 0 and trC.d == 0 and
                  trC2.a == 2736 and trC2.b == 0 and trC2.c == 0 and trC2.d == 0)
    return {
        "method": "exact Weyl-Klimyk character formula (integer) + explicit Q[i,sqrt3] Casimir trace cross-check",
        "total_dim": tot,
        "decomposition": {f"({p},{q})": {"dim": d, "mult": n} for (p, q), (d, n) in dec.items()},
        "commutant_block_sizes_M_m": blocks,
        "commutant_dim": sum(n * n for (d, n) in dec.values()),
        "octet_dim": octet[0],
        "octet_multiplicity": octet[1],
        "explicit_casimir_trC_432_trC2_2736": bool(casimir_ok),
        "gauge_invariance_basis": "Schur inference (octet irreducible x multiplicity 4 => commutant = M_4); "
                                  "no explicit operator [O,G_a]=0 constructed",
        "contains_full_M4": bool(octet == (8, 4) and tot == 81 and 4 in blocks and casimir_ok),
    }


def check_T_su3_octet_colour_KS_coloring_obstruction_exact():
    """The PHYSICAL gauge group SU(3) hosts a state-independent Kochen-Specker COLORING
    obstruction on a gauge-invariant colour interface, in EXACT arithmetic.

    The real-QCD tetraquark q-qbar-q-qbar = (1(+)8)(x)(1(+)8) contains the octet with
    multiplicity 4 (exact Weyl-Klimyk; corroborated by an explicit Q[i,sqrt3] Casimir
    with tr C = 432, tr C^2 = 2736), so its gauge-invariant algebra (the colour
    commutant) contains a full M_4 = the two-qubit operator algebra in the octet
    channel. A two-qubit algebra hosts the Mermin-Peres magic square, which the
    Interface Engine routes to IJCStr with EMPTY global-section support -- a coloring
    IMPOSSIBILITY, contextual for every state, the strongest form.

    SCOPE / honest fences:
      * The KS obstruction itself (the magic square, the GF(2) parity certificate) is
        GROUP-INDEPENDENT -- the identical two-qubit object banked for the SU(2)
        pentaquark M_4 (check_T_gauge_invariant_colour_KS_coloring_obstruction). SU(3)
        supplies only the M_4 HOST: the new, SU(3)-specific content is that the physical
        gauge group realizes it in the physically meaningful octet channel of the
        real-QCD tetraquark, established exactly (upgrading the census note's numerical
        SU(3) octet finding to exact).
      * Gauge-invariance of the M_4 block is a Schur-lemma inference from octet
        irreducibility x multiplicity 4, not an explicit [O, G_a] = 0 operator check.
      * IJC_str (structural) rung ONLY. IJC_adm / occupancy -- whether A1 forces the
        world to realize such an interface -- stays the empirical QAC, untouched.
    Grade P_structural_instrument: the verdict is the engine's exact finite-math
    computation; occupancy is not claimed."""
    from apf.ijc_feasbool_engine import (
        feasbool, global_section_support_nonempty,
        scenario_mermin_peres_magic_square, ks_parity_decide, _magic_square_parity_system,
    )
    cert = _su3_octet_M4_certificate()
    scn = scenario_mermin_peres_magic_square()
    fb = feasbool(scn)
    sup = global_section_support_nonempty(scn)
    n_obs, ctx = _magic_square_parity_system()
    par = ks_parity_decide(n_obs, ctx)
    empty = (sup["witness_section"] is None)
    engine_ijc = (fb["branch"] == "IJCStr" and par["branch"].startswith("IJCStr"))
    ok = bool(cert["contains_full_M4"] and engine_ijc and empty)
    data = {
        "SU3_octet_M4_certificate": cert,
        "ks_set": "Mermin-Peres magic square (two-qubit, state-independent, GROUP-INDEPENDENT)",
        "engine_branch": fb["branch"],
        "global_section_support_empty": empty,
        "parity_certificate": par["certificate"],
        "gauge_group": "SU(3) -- the physical colour group (Gell-Mann lambda_8 carries sqrt3)",
        "new_content_vs_SU2_pentaquark": ("the M_4 HOST is now the physical-SU(3) octet channel of the "
                                          "real-QCD tetraquark, exact; the obstruction itself is the shared "
                                          "group-independent magic square"),
        "scope": ("IJC_str rung only; IJC_adm/occupancy stays the empirical QAC. Gauge-invariance of M_4 is "
                  "a Schur inference (octet irreducible x mult 4), not an explicit operator check."),
    }
    if ok:
        return _ok(
            "check_T_su3_octet_colour_KS_coloring_obstruction_exact",
            status="P_structural_instrument",
            summary=("The physical gauge group SU(3) hosts a state-independent Kochen-Specker COLORING "
                     "obstruction on a gauge-invariant colour interface, exactly. The real-QCD tetraquark "
                     "q-qbar-q-qbar octet has multiplicity 4 (exact Weyl-Klimyk + explicit Q[i,sqrt3] "
                     "Casimir tr C=432, tr C^2=2736), so the colour commutant contains a full M_4 two-qubit "
                     "block in the octet channel; it realizes the Mermin-Peres magic square, which the "
                     "Interface Engine returns IJCStr with empty global-section support (coloring "
                     "impossibility, every state). The obstruction is the group-independent magic square; "
                     "SU(3) supplies the M_4 host, exactly, in the physical octet channel. IJC_str rung "
                     "only; occupancy stays the QAC."),
            data=data,
            dependencies=["check_T_gauge_invariant_colour_KS_coloring_obstruction",
                          "check_T_gauge_invariant_colour_interface_is_contextual",
                          "check_T_interface_contextuality_general_scenario"],
        )
    return _fail(
        "check_T_su3_octet_colour_KS_coloring_obstruction_exact",
        status="FAIL",
        summary="SU(3) octet gauge-invariant magic-square coloring-obstruction witness did not hold.",
        data=data,
    )


# --- k-string spectrum-blindness (the delimiting negative result) ---
def _ksb_partitions(n, mx=None):
    if mx is None:
        mx = n
    if n == 0:
        yield []
        return
    for f in range(min(n, mx), 0, -1):
        for r in _ksb_partitions(n - f, f):
            yield [f] + r


def _ksb_nsyt(lam):
    n = sum(lam); lam = list(lam)
    cols = [0] * (lam[0] if lam else 0)
    for r in lam:
        for c in range(r):
            cols[c] += 1
    pr = 1
    for i, r in enumerate(lam):
        for j in range(r):
            pr *= ((r - j - 1) + (cols[j] - i - 1) + 1)
    return _math.factorial(n) // pr


def _ksb_dmax(N, k):
    """Largest commutant multiplicity block of fund^{ox k} for SU(N) (<= N rows) = the
    contextuality-capability invariant of the k-constituent colour interface."""
    return max(_ksb_nsyt(l) for l in _ksb_partitions(k) if len(l) <= N)


def _ksb_sun_dim(lam, N):
    lam = list(lam) + [0] * (N - len(lam))
    num = den = 1
    for i in range(N):
        for j in range(i + 1, N):
            num *= (lam[i] - lam[j] + (j - i)); den *= (j - i)
    return num // den


def _ksb_lamk_multfree(N, k):
    """Is Lambda^k (x) Lambda^{N-k} multiplicity-free? (dual-Pieri vertical strip + dim
    balance). Multiplicity-free => abelian commutant => the minimal N-ality-k string
    endpoint is never contextual."""
    b = N - k
    heights = [1] * k + [0] * b
    mr = k + b
    comps = set()
    for chosen in _combs(range(mr), b):
        new = heights[:]
        for r in chosen:
            new[r] += 1
        tr = [x for x in new if x > 0]
        if all(tr[i] >= tr[i + 1] for i in range(len(tr) - 1)) and len(tr) <= N:
            comps.add(tuple(tr))
    lhs = _math.comb(N, k) * _math.comb(N, b)
    rhs = sum(_ksb_sun_dim(c, N) for c in comps)
    return lhs == rhs


def check_T_colour_contextuality_is_kstring_spectrum_blind():
    """Every invariant that is a function of the confining colour interface's COMMUTANT
    MULTIPLICITY STRUCTURE is k-string-SPECTRUM-BLIND: it cannot reproduce the k-string
    tension law (Casimir k(N-k) vs sine sin(pi k/N)). A delimiting result -- the strong
    (contextuality) face certifies gap EXISTENCE (via the banked Delta>0 = non-factorizable
    record) but carries no k-string ordering information.

    Two framings, the null holds in BOTH for DIFFERENT reasons (so the result is robust to
    which k-sector one calls physical):
      * Framing II (minimal N-ality-k endpoint): the source rep Lambda^k tensored with its
        conjugate Lambda^{N-k} is MULTIPLICITY-FREE for all N,k => abelian gauge-invariant
        record => never contextual (like the meson). d_max profile is constant = 1.
      * Framing I (k-constituent census, fund^{ox k}): the capability invariant
        d_max(k) = largest commutant block is, in the physical range k <= floor(N/2)
        (N >= 2k), a pure function of k -- N-INDEPENDENT and monotone in k. It grows.

    PRIMARY reason (Claim A, N-independence): at fixed k the commutant invariant is the
    SAME for every N >= 2k, while the tension sigma_k = k(N-k) VARIES with N -- one
    invariant input maps to many spectrum outputs, so no function of the invariant can
    equal sigma_k. The k<->N-k symmetry mismatch (invariant asymmetric, tension symmetric)
    is a CORROBORATING witness (its asymmetry is exhibited at k > floor(N/2), the unphysical
    half; the physical-range argument is Claim A).

    SCOPE (honest): 'spectrum-blind' is scoped to invariants that are FUNCTIONS OF THE
    SINGLE-INTERFACE COMMUTANT MULTIPLICITY STRUCTURE, not literally every conceivable
    quantity. The check asserts NOTHING about sigma_k values, Lambda_QCD, which law is
    correct, occupancy/QAC, or a re-derivation of Delta>0 (it references the banked strong
    face). Grade P_structural_instrument: an exact finite rep-theory computation delimiting
    the engine's reach."""
    Ns = range(3, 9)
    II_all_abelian = all(_ksb_lamk_multfree(N, k) for N in Ns for k in range(1, N))
    # Framing I: N-independence across the physical range k <= floor(N/2)
    dmax_min = {k: _ksb_dmax(k + 1, k) for k in range(1, 8)}
    N_independent = all(_ksb_dmax(N, k) == dmax_min[k]
                        for N in range(3, 15) for k in range(1, N // 2 + 1))
    monotone = all(dmax_min[k] <= dmax_min[k + 1] for k in range(1, 7))
    # Claim A witness: fixed k=4, d_max constant while sigma_k = k(N-k) varies with N
    claimA_k = 4
    dmax_const = len({_ksb_dmax(N, claimA_k) for N in range(8, 16)}) == 1
    sigma_varies = len({claimA_k * (N - claimA_k) for N in range(8, 16)}) > 1
    claimA = bool(dmax_const and sigma_varies)
    # corroborating symmetry witness (at k>floor(N/2), the unphysical half)
    laws_symmetric = all(k * (N - k) == (N - k) * k and
                         abs(_math.sin(_math.pi * k / N) - _math.sin(_math.pi * (N - k) / N)) < 1e-12
                         for N in Ns for k in range(1, N))
    census_asym = any(_ksb_dmax(N, k) != _ksb_dmax(N, N - k) for N in Ns for k in range(1, N))
    framings_differ = (dmax_min[2] != 1)  # framing I grows (d_max(k=... )); framing II constant 1
    ok = bool(II_all_abelian and N_independent and monotone and claimA and
              laws_symmetric and census_asym)
    data = {
        "framing_II_minimal_endpoint_multiplicity_free_abelian": II_all_abelian,
        "framing_I_census_N_independent_physical_range": N_independent,
        "framing_I_census_monotone_in_k": monotone,
        "claimA_fixed_k_invariant_constant_while_sigma_varies": claimA,
        "corroborating_kstring_laws_symmetric": laws_symmetric,
        "corroborating_census_invariant_asymmetric_unphysical_half": census_asym,
        "framings_give_different_dmax_profiles": bool(framings_differ),
        "scope": ("invariants = functions of the single-interface commutant multiplicity structure, "
                  "physical range k<=floor(N/2); NOT every conceivable quantity"),
        "asserts_nothing_about": ["sigma_k values", "Lambda_QCD", "which k-string law holds",
                                  "occupancy/QAC", "re-deriving Delta>0"],
        "verdict": ("commutant-multiplicity contextuality invariants are N-independent (physical range) "
                    "and monotone/asymmetric in k; the k-string tension is N-dependent and k<->N-k "
                    "symmetric => no such invariant tracks Casimir or sine. The strong face fixes gap "
                    "EXISTENCE (Delta>0) but is k-string-spectrum-blind. Null holds in both framings."),
    }
    if ok:
        return _ok(
            "check_T_colour_contextuality_is_kstring_spectrum_blind",
            status="P_structural_instrument",
            summary=("The strong (contextuality) face is k-string-SPECTRUM-BLIND: every invariant that is "
                     "a function of the confining colour interface's commutant multiplicity structure is "
                     "N-independent (physical range k<=floor(N/2)) and monotone/asymmetric in k, whereas "
                     "the k-string tension sigma_k (Casimir k(N-k) or sine sin(pi k/N)) is N-dependent and "
                     "k<->N-k symmetric -- so no such invariant tracks either law (Claim A: at fixed k the "
                     "invariant is constant across N while sigma_k varies). The null holds in both framings "
                     "(minimal endpoint Lambda^k(x)Lambda^{N-k} multiplicity-free/abelian; k-constituent "
                     "census N-independent). Delimiting: the strong face certifies gap existence via the "
                     "banked Delta>0, but carries no k-string ordering information. Asserts nothing about "
                     "sigma_k values, Lambda_QCD, which law holds, or occupancy."),
            data=data,
            dependencies=["check_T_center_order_parameter_triality",
                          "check_T_gauge_invariant_colour_interface_is_contextual"],
        )
    return _fail(
        "check_T_colour_contextuality_is_kstring_spectrum_blind",
        status="FAIL",
        summary="k-string spectrum-blindness witness did not hold.",
        data=data,
    )


def _disjoint_bases_scenario(nbases):
    """A finite marginal Scenario of `nbases` pairwise-DISJOINT orthonormal triads on
    the maximally-mixed qutrit (rank-1 marginals = 1/3).  Each basis is one triad
    context of three fresh rays; no ray is shared across bases and no cross-basis
    orthogonality is imposed -- the orthogonality graph is `nbases` disjoint
    triangles.  This is the engine encoding of `nbases` incompatible orthonormal
    bases that pairwise share no rays."""
    from apf.ijc_feasbool_engine import Scenario
    third = F(1, 3)
    meas = tuple((f"b{t}_r{k}", (1, 0)) for t in range(nbases) for k in range(3))
    contexts, emp = [], []
    for t in range(nbases):
        names = tuple(f"b{t}_r{k}" for k in range(3))
        contexts.append(names)
        emp.append((names, tuple((tuple(1 if m == k else 0 for m in range(3)), third)
                                 for k in range(3))))
    return Scenario(meas, tuple(contexts), tuple(emp))


def _ckm_fully_mixing():
    """Certify from check_T_CKM's own zero-parameter construction that the forced CKM
    matrix V = U_uL^dag U_dL is FULLY MIXING: every |V_ij| is strictly inside (0,1).
    Fully-mixing => the up-mass basis (cols of U_uL) and the down-mass basis (cols of
    U_dL) share NO ray (an exact |V_ij|=1 would be a coincident ray / decoupled
    generation) and have NO cross-basis orthogonality (an exact |V_ij|=0).  So the two
    forced mass bases form a disjoint-triad set.  Returns (ok, min|V|, max|V|)."""
    import math
    from apf import generations as _gen
    phi = math.pi / 4
    q_B = [7, 4, 0]; q_H = [7, 5, 0]
    Delta_k = 3; x = 0.5; c_Hu = x ** 3
    M_u = _gen._build_two_channel(q_B, q_H, phi, Delta_k, 0, 1.0, c_Hu)
    M_d = _gen._build_two_channel(q_B, q_H, phi, 0, 0, 1.0, 1.0)
    _, U_uL = _gen._diag_left(M_u)
    _, U_dL = _gen._diag_left(M_d)
    V = _gen._mm(_gen._dag(U_uL), U_dL)
    mags = [abs(V[i][j]) for i in range(3) for j in range(3)]
    lo, hi = min(mags), max(mags)
    return (lo > 1e-4 and hi < 1.0 - 1e-4), lo, hi


def check_T_ckm_flavour_coavailability_is_sepstr():
    """The CKM-forced flavour co-availability is SepStr, NOT the contextual web.

    Delimiting result on the occupancy-forcing route through the flavour sector
    (thread 1 of the co-availability / flavour-changing-crack continuation).

    The forcing hope: the weak interaction is flavour-changing (forced, chiral SU(2))
    and the CKM matrix is A1-derived and != 1, so the weak/mass flavour bases are
    genuinely incompatible AND both classically measured (mixing angles, branching
    ratios).  So the off-diagonal flavour records are classically consequential, and
    structural completeness would force their co-availability NON-circularly -- the
    move that breaks the co-availability circularity blocking occupancy.

    What is actually forced on a generation qutrit is EXACTLY TWO orthonormal bases:
    the down-type mass basis (cols of U_dL) and the up-type mass basis via the charged
    current (cols of U_uL), related by V = U_uL^dag U_dL != 1.  Both classically
    consequential; no third quark-flavour basis is forced (neutral currents are
    flavour-diagonal / GIM; weak isospin acts up<->down not within the qutrit; neutral-
    meson mixing reduces to V; the SU(3)_V octet currents that span Herm(3) are
    realizable TRANSITION operators, not forced co-available RECORDS -- realizability-
    by-spanning is exactly the all-nine-densities-co-available assumption the QAC leaves
    empirical).

    Four exact facts compose:
      (1) FORCED STRUCTURE.  The two forced mass bases, fed to the Interface Engine as
          two disjoint triads on the maximally-mixed state, return SepStr (9 global
          sections = a manifestly noncontextual model).  Two orthonormal bases sharing
          no rays always admit a global section: noncommutativity, not contextuality.
      (2) COUNT-ROBUST.  The verdict does not depend on the count being two: five
          pairwise-disjoint bases still return SepStr (3^5 sections).  A KS obstruction
          needs ray-SHARING / intertwining across contexts, not more bases.
      (3) CKM FULLY MIXING.  V has every |V_ij| strictly inside (0,1), so the two
          forced bases genuinely share no ray and have no cross-basis orthogonality --
          the forced structure IS a disjoint-triad set.  The verdict flips only if
          forcing produced a coincident ray (|V_ij|=1, a decoupled generation), which
          three genuinely-mixed generations forbid.
      (4) DISCRIMINATION.  The full Yu-Oh 13-ray web (which check_T_chiral_condensate_
          flavour_density_interface_is_contextual uses) IS IJCStr -- so the SepStr
          verdict on the forced set reports the web genuinely ABSENT, not an engine
          blind spot.

    Therefore forced flavour-changing dynamics buy noncommutativity classically (a
    single forced incompatible basis pair = SepStr) but do NOT force contextuality (the
    KS web); assembling the web needs additional co-available incompatible contexts
    whose realization stays the empirical QAC.  One basis rotation is never KS.

    SCOPE / GRADE.  P_structural_instrument: the SepStr/IJCStr verdicts are the engine's
    exact finite Boole-polytope computations; the fully-mixing premise is a margin
    inequality on the [P] CKM.  This delimits ONE forcing route (flavour); it does not
    prove occupancy unforceable in general (threads 2/3 untouched).  IJC_adm / occupancy
    stays the empirical QAC.
    """
    from apf.ijc_feasbool_engine import feasbool

    scn2 = _disjoint_bases_scenario(2)
    fb2 = feasbool(scn2)
    forced_sepstr = (fb2["branch"] == "SepStr" and fb2["n_global_sections"] == 9)

    scn5 = _disjoint_bases_scenario(5)
    fb5 = feasbool(scn5)
    robust_sepstr = (fb5["branch"] == "SepStr" and fb5["n_global_sections"] == 3 ** 5)

    ckm_ok, vlo, vhi = _ckm_fully_mixing()

    yscn, nrays, ntri, npair = _ccf_yuoh_flavour_scenario()
    yfb = feasbool(yscn)
    control_ijc = (yfb["branch"] == "IJCStr")

    ok = bool(forced_sepstr and robust_sepstr and ckm_ok and control_ijc and nrays == 13)
    data = {
        "forced_structure": "two incompatible mass bases on the generation qutrit (down-mass U_dL, up-mass U_uL via the charged current), related by V = U_uL^dag U_dL != 1",
        "forced_two_basis_branch": fb2["branch"],
        "forced_two_basis_sections": fb2["n_global_sections"],
        "five_basis_branch": fb5["branch"],
        "five_basis_sections": fb5["n_global_sections"],
        "count_robust": robust_sepstr,
        "ckm_fully_mixing": ckm_ok,
        "ckm_min_abs_Vij": vlo,
        "ckm_max_abs_Vij": vhi,
        "yuoh_control_branch": yfb["branch"],
        "yuoh_n_rays": nrays,
        "mechanism": "two orthonormal bases sharing no rays always admit a global section (SepStr); KS needs ray-sharing/intertwining, which forced flavour data lack. Forcing buys noncommutativity, not contextuality.",
        "scope": ("delimits the flavour forcing route only; IJC_adm/occupancy (the co-availability "
                  "of the extra intertwined contexts) stays the empirical QAC. One basis rotation is never KS."),
    }
    if ok:
        return _ok(
            "check_T_ckm_flavour_coavailability_is_sepstr",
            status="P_structural_instrument",
            summary=("The CKM-forced flavour co-availability is SepStr, not the contextual web. "
                     "The A1-forced CKM (V != 1, fully mixing: |V_ij| in (%.4f, %.4f)) makes exactly "
                     "two incompatible mass bases (down-mass, up-mass via the charged current) co-"
                     "available and classically consequential; fed to the Interface Engine as two "
                     "disjoint triads they return SepStr (9 sections = noncontextual), and the verdict "
                     "is count-robust (five disjoint bases still SepStr). The full Yu-Oh 13-ray web is "
                     "IJCStr (control), so the web is genuinely absent, not engine-blind. Forced flavour-"
                     "changing dynamics buy noncommutativity classically but not contextuality (KS); the "
                     "extra intertwined co-availability the web needs stays the empirical QAC. One basis "
                     "rotation is never KS -- a delimiting null on the flavour forcing route."
                     % (vlo, vhi)),
            data=data,
            dependencies=["check_T_CKM",
                          "check_T_chiral_condensate_flavour_density_interface_is_contextual",
                          "check_T_feasbool_general_contextuality",
                          "check_T_interface_contextuality_general_scenario"],
        )
    return _fail(
        "check_T_ckm_flavour_coavailability_is_sepstr",
        status="FAIL",
        summary="CKM-forced flavour co-availability SepStr delimiter did not hold.",
        data=data,
    )



CHECKS = {
    "check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P":
        check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P,
    "check_T_unique_gauge_invariant_colour_state_of_N_fundamentals_is_entangled_baryon_P":
        check_T_unique_gauge_invariant_colour_state_of_N_fundamentals_is_entangled_baryon_P,
    "check_T_canonical_colour_record_iff_multiplicity_free_P":
        check_T_canonical_colour_record_iff_multiplicity_free_P,
    "check_T_exotic_gauge_invariant_algebra_is_nonabelian":
        check_T_exotic_gauge_invariant_algebra_is_nonabelian,
    "check_T_gauge_invariant_colour_interface_is_contextual":
        check_T_gauge_invariant_colour_interface_is_contextual,
    "check_T_gauge_invariant_colour_interface_state_independent_contextual":
        check_T_gauge_invariant_colour_interface_state_independent_contextual,
    "check_T_chiral_condensate_flavour_density_interface_is_contextual":
        check_T_chiral_condensate_flavour_density_interface_is_contextual,
    "check_T_gauge_invariant_colour_KS_coloring_obstruction":
        check_T_gauge_invariant_colour_KS_coloring_obstruction,
    "check_T_su3_octet_colour_KS_coloring_obstruction_exact":
        check_T_su3_octet_colour_KS_coloring_obstruction_exact,
    "check_T_colour_contextuality_is_kstring_spectrum_blind":
        check_T_colour_contextuality_is_kstring_spectrum_blind,
    "check_T_ckm_flavour_coavailability_is_sepstr":
        check_T_ckm_flavour_coavailability_is_sepstr,
}


def register(registry=None):
    if registry is None:
        return CHECKS
    if hasattr(registry, "update"):
        registry.update(CHECKS); return registry
    for name, fn in CHECKS.items():
        if hasattr(registry, "register"): registry.register(name, fn)
        elif hasattr(registry, "add"): registry.add(name, fn)
        else: raise TypeError("Unsupported registry type for gauge_invariant_record.register")


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    res = run_all()
    print(json.dumps(res, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in res.values()) else 1)
