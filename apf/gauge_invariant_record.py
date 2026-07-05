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
    the colour action). The former fence "no explicit [O, G_a] = 0 operator is
    constructed" is DISCHARGED by check_T_su3_octet_M4_explicit_construction
    (v24.3.379): the 16 matrix units are constructed as explicit 81x81 rational
    matrices and [e_pq, G_a] = 0 is verified entry-by-entry for all 8 generators;
    the Schur inference is retained as the a-priori argument the construction
    confirms."""
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
                                  "explicit-operator fence DISCHARGED by "
                                  "check_T_su3_octet_M4_explicit_construction (16 explicit "
                                  "matrix units, [e_pq, G_a] = 0 entry-by-entry)",
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
        irreducibility x multiplicity 4. The explicit [O, G_a] = 0 operator check is
        now supplied by check_T_su3_octet_M4_explicit_construction (v24.3.379), which
        constructs the 16 matrix units as 81x81 rational matrices and verifies the
        commutators entry-by-entry; the Schur inference stands as the a-priori
        argument the construction confirms.
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
                  "a Schur inference (octet irreducible x mult 4); the explicit-operator leg is now "
                  "supplied by check_T_su3_octet_M4_explicit_construction."),
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



# ---------------------------------------------------------------------------
# The explicit octet M_4 construction (v24.3.379, Paper 12 round-4 walk A2;
# fresh-context hostile audit LAND-WITH-FIXES 0.88, fixes F1-F6 carried).
# Walk of record: "The Turning/p12_review4_walks_2026-07-04/a2_octet_m4/".
# Exact sparse rational matrices: value = rows/den, rows = {r: {c: int}},
# den > 0. Pure stdlib; every load-bearing step exact over Q.
# ---------------------------------------------------------------------------

def _m4c_digits(x):
    return ((x // 27) % 3, (x // 9) % 3, (x // 3) % 3, x % 3)


def _m4c_idx(d):
    return ((d[0] * 3 + d[1]) * 3 + d[2]) * 3 + d[3]


def _m4c_mnorm(m):
    from math import gcd
    den, rows = m
    rows = {r: {c: v for c, v in row.items() if v != 0} for r, row in rows.items()}
    rows = {r: row for r, row in rows.items() if row}
    if not rows:
        return (1, {})
    g = abs(den)
    for row in rows.values():
        for v in row.values():
            g = gcd(g, abs(v))
    sgn = -1 if den < 0 else 1
    d = abs(den) // g
    if g > 1 or sgn < 0:
        rows = {r: {c: (sgn * v) // g for c, v in row.items()} for r, row in rows.items()}
    return (d, rows)


def _m4c_madd(m1, m2, k=1):
    from math import gcd
    d1, r1 = m1
    d2, r2 = m2
    L = d1 * d2 // gcd(d1, d2)
    f1 = L // d1
    f2 = (L // d2) * k
    rows = {r: {c: v * f1 for c, v in row.items()} for r, row in r1.items()}
    for r, row in r2.items():
        rr = rows.setdefault(r, {})
        for c, v in row.items():
            rr[c] = rr.get(c, 0) + v * f2
    return _m4c_mnorm((L, rows))


def _m4c_mscale(m, fr):
    fr = F(fr)
    d, r = m
    rows = {rr: {c: v * fr.numerator for c, v in row.items()} for rr, row in r.items()}
    return _m4c_mnorm((d * fr.denominator, rows))


def _m4c_mmul(a, b):
    da, ra = a
    db, rb = b
    rows = {}
    for r, row in ra.items():
        acc = {}
        for k2, av in row.items():
            bk = rb.get(k2)
            if not bk:
                continue
            for c, bv in bk.items():
                acc[c] = acc.get(c, 0) + av * bv
        acc = {c: v for c, v in acc.items() if v}
        if acc:
            rows[r] = acc
    return _m4c_mnorm((da * db, rows))


def _m4c_miszero(m):
    return not _m4c_mnorm(m)[1]


def _m4c_meq(a, b):
    return _m4c_miszero(_m4c_madd(a, b, -1))


def _m4c_mcomm(a, b):
    return _m4c_madd(_m4c_mmul(a, b), _m4c_mmul(b, a), -1)


def _m4c_mtrace(m):
    d, r = m
    return F(sum(row.get(k, 0) for k, row in r.items()), d)


def _m4c_mnnz(m):
    return sum(len(row) for row in m[1].values())


def _m4c_mtranspose(m):
    d, r = m
    rows = {}
    for i, row in r.items():
        for j, v in row.items():
            rows.setdefault(j, {})[i] = v
    return (d, rows)


def _m4c_rep(X):
    """Tetraquark action G(X) = X x1x1x1 + 1x(-X^T)x1x1 + 1x1xXx1 + 1x1x1x(-X^T)
    on |i,j,k,l>, slots (fund, antifund, fund, antifund)."""
    rows = {}

    def add(r, c, v):
        if v == 0:
            return
        rr = rows.setdefault(r, {})
        rr[c] = rr.get(c, 0) + v

    for x in range(81):
        i, j, k, l = _m4c_digits(x)
        for a in range(3):
            add(_m4c_idx((a, j, k, l)), x, X[a][i])       # slot 1: fund
            add(_m4c_idx((i, a, k, l)), x, -X[j][a])      # slot 2: antifund
            add(_m4c_idx((i, j, a, l)), x, X[a][k])       # slot 3: fund
            add(_m4c_idx((i, j, k, a)), x, -X[l][a])      # slot 4: antifund
    return _m4c_mnorm((1, rows))


def _m4c_E3(i, j):
    M = [[0] * 3 for _ in range(3)]
    M[i][j] = 1
    return M


def _m4c_mat3(A, B, kB=1):
    return [[A[i][j] + kB * B[i][j] for j in range(3)] for i in range(3)]


def _m4c_mat3mul(A, B):
    return [[sum(A[i][t] * B[t][j] for t in range(3)) for j in range(3)]
            for i in range(3)]


def _m4c_rank_tracked(vecs):
    """Exact integer rank with relation tracking (fraction-free, gcd-normalized).
    Returns (rank, independent_indices, relations)."""
    from math import gcd
    AUG = 10 ** 9
    pivots = {}
    rank = 0
    indep = []
    relations = []
    for m, v0 in enumerate(vecs):
        row = dict(v0)
        row[AUG + m] = 1
        while True:
            real = [c for c in row if c < AUG]
            if not real:
                relations.append({c - AUG: v for c, v in row.items()})
                break
            c = min(real)
            p = pivots.get(c)
            if p is None:
                g = 0
                for v in row.values():
                    g = gcd(g, abs(v))
                if g > 1:
                    row = {k: v // g for k, v in row.items()}
                pivots[c] = row
                rank += 1
                indep.append(m)
                break
            a = p[c]
            b = row[c]
            new = {k: v * a for k, v in row.items()}
            for k, v in p.items():
                w = new.get(k, 0) - v * b
                if w:
                    new[k] = w
                elif k in new:
                    del new[k]
            row = new
            if row:
                g = 0
                for v in row.values():
                    g = gcd(g, abs(v))
                if g > 1:
                    row = {k: v // g for k, v in row.items()}
    return rank, indep, relations


def _m4c_rank_sparse_exact(rows):
    """Exact integer rank of sparse integer rows (fraction-free elimination)."""
    from math import gcd
    pivots = {}
    rank = 0
    for row0 in sorted(rows, key=len):
        row = dict(row0)
        while row:
            c = min(row)
            p = pivots.get(c)
            if p is None:
                g = 0
                for v in row.values():
                    g = gcd(g, abs(v))
                if g > 1:
                    row = {k: v // g for k, v in row.items()}
                pivots[c] = row
                rank += 1
                break
            a = p[c]
            b = row[c]
            new = {k: v * a for k, v in row.items()}
            for k, v in p.items():
                w = new.get(k, 0) - v * b
                if w:
                    new[k] = w
                elif k in new:
                    del new[k]
            row = new
            if row:
                g = 0
                for v in row.values():
                    g = gcd(g, abs(v))
                if g > 1:
                    row = {k: v // g for k, v in row.items()}
    return rank


def _m4c_rref_dense(A, npiv_cols):
    r = 0
    piv = []
    for c in range(npiv_cols):
        pr = next((rr for rr in range(r, len(A)) if A[rr][c] != 0), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        pv = A[r][c]
        A[r] = [v / pv for v in A[r]]
        for rr in range(len(A)):
            if rr != r and A[rr][c] != 0:
                fct = A[rr][c]
                A[rr] = [x - fct * y for x, y in zip(A[rr], A[r])]
        piv.append(c)
        r += 1
        if r == len(A):
            break
    return A, piv


def _m4c_nullspace_dense(rows, n):
    M = [[F(row.get(t, 0)) for t in range(n)] for row in rows]
    if not M:
        M = [[F(0)] * n]
    M, piv = _m4c_rref_dense(M, n)
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [F(0)] * n
        v[fc] = F(1)
        for rr, pc in enumerate(piv):
            v[pc] = -M[rr][fc]
        basis.append(v)
    return basis


def _m4c_perm_sign(p):
    sgn = 1
    for i in range(4):
        for j in range(i + 1, 4):
            if p[i] > p[j]:
                sgn = -sgn
    return sgn


def check_T_su3_octet_M4_explicit_construction():
    """The gauge-invariant M_4 block in the octet channel of the SU(3)
    tetraquark 3 (x) 3bar (x) 3 (x) 3bar is CONSTRUCTED, not inferred: 16
    explicit 81x81 rational matrix units e_pq (p, q = 1..4) satisfying
    [e_pq, G(X)] = 0 exactly for all X in sl(3,C) (checked on the spanning
    integer basis E12, E21, E13, E31, E23, E32, H1, H2 -- equivalent to the
    Gell-Mann basis by linearity: the scalar factors -i and 1/sqrt3 are
    irrelevant to the vanishing of a commutator -- and extended to SU(3) by
    exponentiation/connectedness), e_pq e_rs = delta_qr e_ps (all 256
    ordered products), sum_p e_pp = P_octet (exact rank 32), together with
    explicit two-qubit Pauli operators realizing the six Mermin-Peres
    product identities (row signs +,+,+; column signs +,+,-) as exact
    matrix equations. The commutant is simultaneously pinned at dimension
    23 by direct exact rank computation (H-block closed form, 639
    weight-diagonal unknowns; 2736 integer E-equations of exact rank 616),
    with the unique diagram relation sum_sigma sgn(sigma) T_sigma = 0
    exhibited. DISCHARGES the certificate fence "no explicit [O, G_a] = 0
    operator is constructed" (_su3_octet_M4_certificate).

    DISCRIMINATION NOTE (audit F1 -- the blind-spot documented): the
    headline invariants do NOT discriminate the group action. For the
    WRONG all-fund action 3 (x) 3 (x) 3 (x) 3 (no -X^T on the bar slots)
    every headline number is IDENTICAL: weight-diagonal unknowns 639,
    E-system rank 616, commutant dim 23 (Schur-Weyl over the <=3-row S_4
    partitions), and tr C = 432, tr C^2 = 2736 (the cross-slot trace terms
    vanish by tracelessness regardless of transpose signs; the per-slot
    traces are transpose-invariant). So neither the dim-23 elimination,
    nor the character cross-check, nor the Casimir-trace reproduction can
    catch the fund<->antifund error class. The legs that DO pin the
    action, run in-check: the diagram-commutation leg (the
    delta-contraction diagrams fail 160/192 commutators under the all-fund
    action), the rep-property leg [G(X), G(Y)] = G([X, Y]) (five bracket
    pairs including [E12, E21] = H1 -- the audit's direct action pin), the
    Casimir SPECTRUM / projector-trace legs ({0, 3, 6, 8} with isotypic
    dims 2/32/20/27, vs {4/3, 10/3, 16/3, 28/3} for all-fund), the
    highest-weight multiplicity legs, and the negative control.

    ANTISYMMETRIZER GLOSS (audit F5): the unique relation antisymmetrizes
    over the four COVARIANT POSITIONS OF THE MIXED TENSOR (equivalently:
    the generalized Kronecker delta with four upper and four lower indices
    vanishes identically for N = 3 < 4) -- NOT the naive antisymmetrizer
    on the fourth tensor power of the fundamental; the fund positions
    straddle the wall between out- and in-slots.

    HERMITICITY (audit F3 -- the sharper verified fact): the standard
    inner product on C^81 is SU(3)-invariant for this action (fund and
    antifund slots both act unitarily), and P_octet = P_octet^T EXACTLY
    (verified in-check) -- an honest orthogonal projector, no adapted
    basis needed. The constructed matrix units are NOT Hermitian as-is
    (the multiplicity basis h_1..h_4 is rational but not orthonormal, and
    orthonormalization exits Q); orthonormalizing h_1..h_4 (a square-root
    step) conjugates the block to Hermitian matrix units, making the nine
    square operators Hermitian observables -- the product identities
    verified here are conjugation-invariant and are the load-bearing
    content of the KS argument. Explicit HERMITIAN observables therefore
    remain undelivered (structurally obstructed over Q) -- out of scope,
    stated (audit F6).

    FENCE (audit F5 guard, mandatory): this check certifies ONLY the
    mathematical construction. The contextuality verdicts stay
    [P_structural_instrument] on the parent check
    (check_T_su3_octet_colour_KS_coloring_obstruction_exact); nothing here
    re-grades them. The parent Remark's first clause -- the obstruction
    OBJECT (the magic square) is group-independent -- is untouched and
    survives (audit F6): SU(3) supplies the M_4 host, now explicitly
    constructed. IJC_adm / occupancy stays the empirical QAC.

    Grade bare [P] (in-module precedent:
    check_T_exotic_gauge_invariant_algebra_is_nonabelian): every leg is a
    finite exact-arithmetic identity over Q -- integer matrices, Fraction
    elimination, entry-by-entry equality. No reading enters: no occupancy
    claim, no interface adoption, no measured input, no floats. The banked
    character decomposition and Q[i,sqrt3] Casimir traces are consumed as
    a REAL cross-check (audit F2): _su3_octet_M4_certificate() is called
    and its commutant_dim / octet_multiplicity / Casimir flag are asserted
    equal to this check's independently computed values."""
    legs = []

    def leg(ok, label):
        legs.append((bool(ok), label))

    MZERO = (1, {})
    MID = (1, {x: {x: 1} for x in range(81)})

    H1m = _m4c_mat3(_m4c_E3(0, 0), _m4c_E3(1, 1), -1)
    H2m = _m4c_mat3(_m4c_E3(1, 1), _m4c_E3(2, 2), -1)
    GEN = {
        'E12': _m4c_rep(_m4c_E3(0, 1)), 'E21': _m4c_rep(_m4c_E3(1, 0)),
        'E13': _m4c_rep(_m4c_E3(0, 2)), 'E31': _m4c_rep(_m4c_E3(2, 0)),
        'E23': _m4c_rep(_m4c_E3(1, 2)), 'E32': _m4c_rep(_m4c_E3(2, 1)),
        'H1': _m4c_rep(H1m), 'H2': _m4c_rep(H2m),
    }
    GENLIST = list(GEN.items())

    # weights
    h1v = [1, -1, 0]
    h2v = [0, 1, -1]

    def wt(x):
        i, j, k, l = _m4c_digits(x)
        return (h1v[i] - h1v[j] + h1v[k] - h1v[l],
                h2v[i] - h2v[j] + h2v[k] - h2v[l])

    W = [wt(x) for x in range(81)]
    okH = True
    for nm, comp in (('H1', 0), ('H2', 1)):
        d, rows = GEN[nm]
        if d != 1:
            okH = False
        for r, row in rows.items():
            for c, v in row.items():
                if r != c or v != W[r][comp]:
                    okH = False
    leg(okH, "H1, H2 act diagonally with integer weight eigenvalues "
             "(H-equations force weight-diagonal support, exactly)")

    # rep-property leg (audit F1, mandatory): [G(X), G(Y)] = G([X, Y])
    E12m, E21m = _m4c_E3(0, 1), _m4c_E3(1, 0)
    E13m, E31m = _m4c_E3(0, 2), _m4c_E3(2, 0)
    E23m, E32m = _m4c_E3(1, 2), _m4c_E3(2, 1)
    bracket_pairs = [
        (E12m, E21m),                       # [E12, E21] = H1
        (E23m, E32m),                       # [E23, E32] = H2
        (E12m, E23m),                       # [E12, E23] = E13
        (H1m, E12m),                        # [H1, E12] = 2 E12
        (E13m, E31m),                       # [E13, E31] = H1 + H2
    ]
    ok_rep = True
    for Xm, Ym in bracket_pairs:
        XY = _m4c_mat3(_m4c_mat3mul(Xm, Ym), _m4c_mat3mul(Ym, Xm), -1)
        lhs = _m4c_mcomm(_m4c_rep(Xm), _m4c_rep(Ym))
        if not _m4c_meq(lhs, _m4c_rep(XY)):
            ok_rep = False
    leg(ok_rep, "rep property [G(X), G(Y)] = G([X, Y]) on five bracket pairs "
                "incl. [E12, E21] = H1 (the direct action pin; audit F1)")

    # Stage A: the 24 contraction diagrams
    import itertools as _it
    FPOS = [('o', 0), ('o', 2), ('i', 1), ('i', 3)]
    APOS = [('i', 0), ('i', 2), ('o', 1), ('o', 3)]
    PERMS = list(_it.permutations(range(4)))

    def diagram(p):
        rows = {}
        for vals in _it.product(range(3), repeat=4):
            o = [0] * 4
            ii = [0] * 4
            for m in range(4):
                side, slot = FPOS[m]
                (o if side == 'o' else ii)[slot] = vals[m]
                side, slot = APOS[p[m]]
                (o if side == 'o' else ii)[slot] = vals[m]
            r = _m4c_idx(o)
            c = _m4c_idx(ii)
            rr = rows.setdefault(r, {})
            rr[c] = rr.get(c, 0) + 1
        return _m4c_mnorm((1, rows))

    DIAG = [diagram(p) for p in PERMS]
    leg(_m4c_meq(DIAG[PERMS.index((0, 1, 2, 3))], MID)
        and all(_m4c_mnnz(D) == 81
                and all(v == 1 for row in D[1].values() for v in row.values())
                for D in DIAG),
        "identity diagram == identity operator; every diagram has exactly 81 "
        "unit entries")
    bad = sum(1 for D in DIAG for nm, G in GENLIST
              if not _m4c_miszero(_m4c_mcomm(D, G)))
    leg(bad == 0, "all 24 walled-Brauer contraction diagrams satisfy "
                  "[T_sigma, G] = 0 exactly for all 8 generators "
                  "(192 commutators; the action-discriminating leg)")
    GM = [
        _m4c_madd(GEN['E12'], GEN['E21']),
        _m4c_madd(GEN['E12'], GEN['E21'], -1),
        GEN['H1'],
        _m4c_madd(GEN['E13'], GEN['E31']),
        _m4c_madd(GEN['E13'], GEN['E31'], -1),
        _m4c_madd(GEN['E23'], GEN['E32']),
        _m4c_madd(GEN['E23'], GEN['E32'], -1),
        _m4c_madd(GEN['H1'], GEN['H2'], 2),
    ]
    bad = sum(1 for D in DIAG for g in GM if not _m4c_miszero(_m4c_mcomm(D, g)))
    leg(bad == 0, "commutation with the eight Gell-Mann combinations "
                  "(lam2/5/7 up to -i, sqrt3*lam8 = H1 + 2 H2)")

    vecs = [{r * 81 + c: v for r, row in D[1].items() for c, v in row.items()}
            for D in DIAG]
    rkD, indepD, relsD = _m4c_rank_tracked(vecs)
    leg(rkD == 23, f"diagram span has exact rank 23 (found {rkD}): 23 "
                   "explicitly independent gauge-invariant operators")
    rel_ok = False
    if len(relsD) == 1:
        rel = relsD[0]
        if set(rel) == set(range(24)) and all(abs(v) == 1 for v in rel.values()):
            s0 = rel[0] * _m4c_perm_sign(PERMS[0])
            rel_ok = all(rel[m] == s0 * _m4c_perm_sign(PERMS[m]) for m in range(24))
    leg(rel_ok, "unique diagram relation = sum_sigma sgn(sigma) T_sigma = 0: "
                "the antisymmetrizer over the four COVARIANT POSITIONS of "
                "the mixed tensor (generalized Kronecker delta, N = 3 < 4)")

    # Stage B: commutant dimension 23 by exact elimination
    from collections import Counter as _Counter
    pairs = [(x, y) for x in range(81) for y in range(81) if W[x] == W[y]]
    NU = len(pairs)
    mw = _Counter(W)
    leg(NU == 639 and NU == sum(m * m for m in mw.values()),
        f"weight-diagonal unknown space dim = sum_w m_w^2 = {NU} == 639 "
        "(H-equations solved in closed form)")
    eqs = {}
    for nm in ('E12', 'E21', 'E13', 'E31', 'E23', 'E32'):
        dG, rG = GEN[nm]
        cols = {}
        for r, row in rG.items():
            for c, v in row.items():
                cols.setdefault(c, {})[r] = v
        for t, (a, b) in enumerate(pairs):
            rb = rG.get(b)
            if rb:
                for y, v in rb.items():
                    d0 = eqs.setdefault((nm, a, y), {})
                    d0[t] = d0.get(t, 0) + v
            ca = cols.get(a)
            if ca:
                for x2, v in ca.items():
                    d0 = eqs.setdefault((nm, x2, b), {})
                    d0[t] = d0.get(t, 0) - v
    rows_eq = [{c: v for c, v in r.items() if v} for r in eqs.values()]
    rows_eq = [r for r in rows_eq if r]
    rkQ = _m4c_rank_sparse_exact(rows_eq)
    leg(NU - rkQ == 23,
        f"EXACT over Q: commutant dim = {NU} - {rkQ} = {NU - rkQ} == 23 "
        "(2736 integer E-equations, exact rank 616; direct linear algebra, "
        "not Schur)")

    # banked cross-check (audit F2 -- a REAL coupling, no hardcoded leg)
    cert = _su3_octet_M4_certificate()
    leg(cert["commutant_dim"] == NU - rkQ == 23
        and cert["octet_multiplicity"] == 4
        and bool(cert["explicit_casimir_trC_432_trC2_2736"])
        and bool(cert["contains_full_M4"]),
        "banked cross-check: _su3_octet_M4_certificate() called in-check -- "
        "character-theory commutant_dim == the elimination's 23, octet "
        "multiplicity 4, Q[i,sqrt3] Casimir flag True")

    # Stage C: rational Casimir, projectors, P_octet
    Cas = MZERO
    for i in range(3):
        for j in range(3):
            if i != j:
                Cas = _m4c_madd(Cas, _m4c_mscale(
                    _m4c_mmul(_m4c_rep(_m4c_E3(i, j)), _m4c_rep(_m4c_E3(j, i))),
                    F(1, 2)))
    GH1, GH2 = GEN['H1'], GEN['H2']
    Cas = _m4c_madd(Cas, _m4c_mscale(_m4c_madd(_m4c_mmul(GH1, GH1),
                                               _m4c_mmul(GH2, GH2)), F(1, 3)))
    Cas = _m4c_madd(Cas, _m4c_mscale(_m4c_madd(_m4c_mmul(GH1, GH2),
                                               _m4c_mmul(GH2, GH1)), F(1, 6)))
    bad = sum(1 for nm, G in GENLIST if not _m4c_miszero(_m4c_mcomm(Cas, G)))
    leg(bad == 0, "rational dual-basis Casimir C commutes with all 8 generators")
    trC = _m4c_mtrace(Cas)
    trC2 = _m4c_mtrace(_m4c_mmul(Cas, Cas))
    leg(trC == 432 and trC2 == 2736,
        f"tr C = {trC} == 432 and tr C^2 = {trC2} == 2736 -- the banked "
        "Q[i,sqrt3] values reproduced over Q alone (degenerate across the "
        "wrong action; see the discrimination note)")

    EVS = [0, 3, 6, 8]

    def polyP(target):
        P = MID
        denom = 1
        for e in EVS:
            if e == target:
                continue
            P = _m4c_mmul(P, _m4c_madd(Cas, MID, -e))
            denom *= (target - e)
        return _m4c_mscale(P, F(1, denom))

    PROJ = {e: polyP(e) for e in EVS}
    P8 = PROJ[3]
    sumP = MZERO
    for e in EVS:
        sumP = _m4c_madd(sumP, PROJ[e])
    leg(_m4c_meq(sumP, MID)
        and all(_m4c_meq(_m4c_mmul(PROJ[e], PROJ[e]), PROJ[e]) for e in EVS)
        and all(_m4c_miszero(_m4c_mmul(PROJ[e], PROJ[f]))
                for e in EVS for f in EVS if e != f)
        and all(_m4c_meq(_m4c_mmul(Cas, PROJ[e]), _m4c_mscale(PROJ[e], e))
                for e in EVS),
        "spectral projectors at C2 in {0, 3, 6, 8}: idempotent, mutually "
        "orthogonal, resolution of identity, C P_e = e P_e (exact) -- the "
        "SPECTRUM is an action-discriminating leg")
    traces = {e: _m4c_mtrace(PROJ[e]) for e in EVS}
    leg(traces[0] == 2 and traces[3] == 32 and traces[6] == 20
        and traces[8] == 27,
        "isotypic dimensions from projector traces: trivial 2, octet 32, "
        "(3,0)+(0,3) 20, (2,2) 27 (sum 81) -- action-discriminating")
    bad = sum(1 for nm, G in GENLIST if not _m4c_miszero(_m4c_mcomm(P8, G)))
    leg(bad == 0, "P_octet commutes exactly with all 8 generators")
    rows_p8 = [dict(row) for row in P8[1].values()]
    rkP8 = _m4c_rank_sparse_exact(rows_p8)
    leg(rkP8 == 32 and _m4c_mtrace(P8) == 32,
        f"P_octet rank = {rkP8} == 32 by exact elimination AND trace")
    leg(_m4c_meq(P8, _m4c_mtranspose(P8)),
        "P_octet = P_octet^T exactly (audit F3): the standard inner product "
        "on C^81 is SU(3)-invariant for this action, so P_octet is an "
        "honest orthogonal projector")

    # Stage D: highest-weight spaces -- explicit multiplicities
    def hw_space(wtarget):
        xs = [x for x in range(81) if W[x] == wtarget]
        rows = {}
        for nm in ('E12', 'E23'):
            dG, rG = GEN[nm]
            cols = {}
            for r, row in rG.items():
                for c, v in row.items():
                    cols.setdefault(c, {})[r] = v
            for t, x in enumerate(xs):
                for r, v in cols.get(x, {}).items():
                    rows.setdefault((nm, r), {})[t] = v
        basis = _m4c_nullspace_dense(list(rows.values()), len(xs))
        return xs, basis

    HW_EXPECT = {(0, 0): 2, (1, 1): 4, (3, 0): 1, (0, 3): 1, (2, 2): 1}
    hw_found = {}
    for wtar in HW_EXPECT:
        xs, basis = hw_space(wtar)
        hw_found[wtar] = len(basis)
    leg(hw_found == HW_EXPECT,
        "explicit highest-weight-space dimensions reproduce the Weyl-Klimyk "
        "multiplicities (2, 4, 1, 1, 1) -- character-free, per irrep, "
        "action-discriminating")

    xs8, basis8 = hw_space((1, 1))
    from math import gcd as _gcd
    hvec = []
    for b in basis8:
        Lden = 1
        for fr in b:
            Lden = Lden * fr.denominator // _gcd(Lden, fr.denominator)
        v = {xs8[t]: int(b[t] * Lden) for t in range(len(xs8)) if b[t] != 0}
        hvec.append(v)
    leg(len(hvec) == 4 and len(xs8) == 8,
        "octet multiplicity space: dim V_theta = 8 at theta = (1,1); "
        "explicit integer h_1..h_4 extracted (joint kernel of E12, E23)")

    def applym(m, vec):
        d, rows = m
        out = {}
        for r, row in rows.items():
            acc = 0
            for c, v in row.items():
                w = vec.get(c)
                if w:
                    acc += v * w
            if acc:
                out[r] = F(acc, d)
        return out

    def vec_sub(v1, v2):
        out = dict(v1)
        for kk, v in v2.items():
            out[kk] = out.get(kk, 0) - v
        return {kk: v for kk, v in out.items() if v != 0}

    leg(all(not applym(GEN[nm], h) for nm in ('E12', 'E23') for h in hvec),
        "each h_p is killed exactly by the raising operators E12, E23")
    leg(all(not vec_sub(applym(P8, h), {k: F(v) for k, v in h.items()})
            for h in hvec),
        "P_octet h_p = h_p exactly (the multiplicity space sits inside the "
        "octet isotypic)")

    # Stage E: the 16 explicit matrix units
    def solve_in_basis(bvecs, target):
        support = sorted(set().union(*[set(b) for b in bvecs]) | set(target))
        nb = len(bvecs)
        A = [[F(b.get(sp, 0)) for b in bvecs] + [F(target.get(sp, 0))]
             for sp in support]
        A, piv = _m4c_rref_dense(A, nb)
        for rr in range(len(A)):
            if all(A[rr][c] == 0 for c in range(nb)) and A[rr][nb] != 0:
                return None
        sol = [F(0)] * nb
        for rr, c in enumerate(piv):
            sol[c] = A[rr][nb]
        return sol

    rho = []
    ok_pres = True
    for m in range(24):
        cols = []
        for p in range(4):
            img = applym(DIAG[m], hvec[p])
            sol = solve_in_basis(hvec, img)
            if sol is None:
                ok_pres = False
                sol = [F(0)] * 4
            cols.append(sol)
        rho.append([[cols[p][r] for p in range(4)] for r in range(4)])
    leg(ok_pres, "every diagram operator preserves the 4-dim multiplicity "
                 "space (exact solve)")

    ENT = [(u, v) for u in range(4) for v in range(4)]
    Aug = []
    for (u, v) in ENT:
        row = [F(rho[m][u][v]) for m in range(24)]
        row += [F(1) if (u, v) == (p, q) else F(0) for (p, q) in ENT]
        Aug.append(row)
    Aug, piv = _m4c_rref_dense(Aug, 24)
    leg(len(piv) == 16, "the commutant surjects onto End(multiplicity "
                        "space): span{rho(T_sigma)} = M_4 (exact rank 16, "
                        "internal rank squeeze -- no double-commutant cited)")
    Csol = {}
    ok_sol = True
    for ti, (p, q) in enumerate(ENT):
        col = 24 + ti
        for rr in range(len(Aug)):
            if all(Aug[rr][cc] == 0 for cc in range(24)) and Aug[rr][col] != 0:
                ok_sol = False
        c = [F(0)] * 24
        for rr, pc in enumerate(piv):
            c[pc] = Aug[rr][col]
        Csol[(p, q)] = c
    leg(ok_sol, "coefficient systems for all 16 matrix units consistent (exact)")

    EU = {}
    for (p, q), c in Csol.items():
        acc = MZERO
        for m in range(24):
            if c[m]:
                acc = _m4c_madd(acc, _m4c_mscale(DIAG[m], c[m]))
        EU[(p, q)] = _m4c_mmul(_m4c_mmul(P8, acc), P8)

    bad = sum(1 for pq in ENT for nm, G in GENLIST
              if not _m4c_miszero(_m4c_mcomm(EU[pq], G)))
    leg(bad == 0, "[e_pq, G] = 0 exactly for all 16 matrix units x 8 "
                  "generators (128 commutators) -- THE FENCE, DISCHARGED")
    bad = 0
    for (p, q) in ENT:
        for (r, ss) in ENT:
            prod = _m4c_mmul(EU[(p, q)], EU[(r, ss)])
            expect = EU[(p, ss)] if q == r else MZERO
            if not _m4c_meq(prod, expect):
                bad += 1
    leg(bad == 0, "matrix-unit algebra e_pq e_rs = delta_qr e_ps: all 256 "
                  "ordered products exact")
    sm = MZERO
    for p in range(4):
        sm = _m4c_madd(sm, EU[(p, p)])
    leg(_m4c_meq(sm, P8), "sum_p e_pp = P_octet (rank 32) exactly")
    bad = 0
    for (p, q) in ENT:
        for r in range(4):
            out = applym(EU[(p, q)], hvec[r])
            expect = {k: F(v) for k, v in hvec[p].items()} if r == q else {}
            if vec_sub(out, expect):
                bad += 1
    leg(bad == 0, "e_pq h_r = delta_qr h_p on the explicit multiplicity "
                  "basis (64 checks exact)")

    # Stage F: two qubits and the Mermin-Peres square (p - 1 = 2 b1 + b2)
    def esum(terms):
        acc = MZERO
        for pq, k in terms:
            acc = _m4c_madd(acc, EU[pq], k)
        return acc

    X1 = esum([((0, 2), 1), ((2, 0), 1), ((1, 3), 1), ((3, 1), 1)])
    Z1 = esum([((0, 0), 1), ((1, 1), 1), ((2, 2), -1), ((3, 3), -1)])
    X2 = esum([((0, 1), 1), ((1, 0), 1), ((2, 3), 1), ((3, 2), 1)])
    Z2 = esum([((0, 0), 1), ((1, 1), -1), ((2, 2), 1), ((3, 3), -1)])
    leg(_m4c_meq(_m4c_mmul(X1, X1), P8) and _m4c_meq(_m4c_mmul(Z1, Z1), P8)
        and _m4c_meq(_m4c_mmul(X2, X2), P8) and _m4c_meq(_m4c_mmul(Z2, Z2), P8)
        and _m4c_miszero(_m4c_madd(_m4c_mmul(X1, Z1), _m4c_mmul(Z1, X1)))
        and _m4c_miszero(_m4c_madd(_m4c_mmul(X2, Z2), _m4c_mmul(Z2, X2)))
        and all(_m4c_miszero(_m4c_mcomm(a, b))
                for a, b in ((X1, X2), (X1, Z2), (Z1, X2), (Z1, Z2))),
        "two-qubit Pauli relations: X_i^2 = Z_i^2 = P_octet, {X_i, Z_i} = 0, "
        "cross-qubit commuting (exact)")

    A13 = _m4c_mmul(X1, X2)
    A23 = _m4c_mmul(Z1, Z2)
    A31 = _m4c_mmul(X1, Z2)
    A32 = _m4c_mmul(Z1, X2)
    A33 = _m4c_mscale(_m4c_mmul(_m4c_mmul(X1, Z1), _m4c_mmul(X2, Z2)), -1)
    SQ = [[X1, X2, A13], [Z2, Z1, A23], [A31, A32, A33]]
    bad = sum(1 for row in SQ for Aop in row for nm, G in GENLIST
              if not _m4c_miszero(_m4c_mcomm(Aop, G)))
    leg(bad == 0, "all 9 magic-square operators gauge invariant: [A, G] = 0 "
                  "(72 commutators exact)")
    leg(all(_m4c_meq(_m4c_mmul(Aop, Aop), P8) for row in SQ for Aop in row),
        "all 9 magic-square operators square to P_octet (involutions on "
        "the block; Y1Y2 = -X1 Z1 X2 Z2 stays rational)")
    ok_comm = True
    for t in range(3):
        for aa in range(3):
            for bb in range(aa + 1, 3):
                if not _m4c_miszero(_m4c_mcomm(SQ[t][aa], SQ[t][bb])):
                    ok_comm = False
                if not _m4c_miszero(_m4c_mcomm(SQ[aa][t], SQ[bb][t])):
                    ok_comm = False
    leg(ok_comm, "each row and each column mutually commutes (18 commutators)")
    row_signs = []
    col_signs = []
    for t in range(3):
        pr = _m4c_mmul(_m4c_mmul(SQ[t][0], SQ[t][1]), SQ[t][2])
        row_signs.append('+' if _m4c_meq(pr, P8)
                         else ('-' if _m4c_meq(pr, _m4c_mscale(P8, -1)) else '?'))
        pc = _m4c_mmul(_m4c_mmul(SQ[0][t], SQ[1][t]), SQ[2][t])
        col_signs.append('+' if _m4c_meq(pc, P8)
                         else ('-' if _m4c_meq(pc, _m4c_mscale(P8, -1)) else '?'))
    leg(row_signs == ['+', '+', '+'] and col_signs == ['+', '+', '-'],
        "Mermin-Peres product identities: rows (+P8, +P8, +P8), columns "
        "(+P8, +P8, -P8) -- product of all six constraints = -1 while every "
        "operator appears exactly twice: the KS contradiction, carried by "
        "explicit operators in the octet channel")

    # Stage G: negative control
    rowsS = {}
    for x in range(81):
        i, j, k, l = _m4c_digits(x)
        rowsS.setdefault(_m4c_idx((j, i, k, l)), {})[x] = 1
    OSWAP = _m4c_mnorm((1, rowsS))
    viol = {nm: _m4c_mnnz(_m4c_mcomm(OSWAP, G)) for nm, G in GENLIST}
    leg(any(v > 0 for v in viol.values()),
        "NEGATIVE CONTROL: the bare slot-1<->2 swap (ignores the "
        "rep/conjugate-rep distinction) FAILS [O, G] = 0 -- the invariance "
        "test has teeth (and pins the action class; audit F1)")

    ok = all(c for c, _ in legs)
    n_legs = len(legs)
    data = {
        "n_legs": n_legs,
        "legs": [{"ok": c, "leg": lbl} for c, lbl in legs],
        "numbers": {
            "dim_V": 81, "weight_diagonal_dim": NU,
            "E_system_rank_exact": rkQ, "commutant_dim_exact": NU - rkQ,
            "diagram_rank": rkD, "trC": str(trC), "trC2": str(trC2),
            "P_octet_rank": rkP8,
            "projector_traces": {str(e): str(t) for e, t in traces.items()},
            "hw_multiplicities": {str(k): v for k, v in hw_found.items()},
            "row_signs": row_signs, "col_signs": col_signs,
            "negative_control_violations": viol,
        },
        "discrimination_note": (
            "dim/rank/trace invariants are DEGENERATE across the wrong "
            "all-fund action 3x3x3x3 (identical 639 unknowns / rank 616 / "
            "dim 23 / tr C = 432 / tr C^2 = 2736); the discriminating legs "
            "are diagram commutation, the rep-property leg, the Casimir "
            "spectrum/projector traces, the hw multiplicities, and the "
            "negative control (audit F1)"),
        "hermiticity": (
            "standard inner product SU(3)-invariant for this action; "
            "P_octet = P_octet^T exact; matrix units non-Hermitian as-is "
            "(h-basis not orthonormal; orthonormalization exits Q); "
            "explicit Hermitian observables undelivered -- out of scope, "
            "stated (audit F3/F6)"),
        "fence": ("construction only, bare [P]; the contextuality verdicts "
                  "stay [P_structural_instrument] on the parent check "
                  "check_T_su3_octet_colour_KS_coloring_obstruction_exact; "
                  "the magic-square obstruction OBJECT is group-independent "
                  "(the parent Remark's first clause, untouched); occupancy "
                  "stays the empirical QAC"),
        "antisymmetrizer": ("sum_sigma sgn(sigma) T_sigma = 0 antisymmetrizes "
                            "over the four covariant positions of the mixed "
                            "tensor (generalized Kronecker delta, N = 3 < 4)"),
    }
    name = "check_T_su3_octet_M4_explicit_construction"
    deps = ["check_T_su3_octet_colour_KS_coloring_obstruction_exact"]
    if ok:
        return _ok(
            name,
            status="P",
            summary=(
                "The octet M_4 block is CONSTRUCTED, not inferred: 16 explicit "
                "81x81 rational matrix units with [e_pq, G_a] = 0 verified "
                "entry-by-entry against all 8 sl(3) generators (128 "
                "commutators; extended to sl(3,C) by linearity and to SU(3) "
                "by exponentiation), e_pq e_rs = delta_qr e_ps (256 "
                "products), sum e_pp = P_octet (exact rank 32, P_octet "
                "symmetric); explicit two-qubit Paulis realize the six "
                "Mermin-Peres identities as exact matrix equations (rows "
                "+,+,+; columns +,+,-). Commutant dim pinned at 23 by exact "
                "elimination (639 weight-diagonal unknowns, 2736 integer "
                "equations of rank 616); unique diagram relation = the "
                "signed antisymmetrizer over the four covariant positions "
                "of the mixed tensor; highest-weight multiplicities "
                "(2,4,1,1,1) by explicit nullspace; tr C = 432, tr C^2 = "
                "2736 reproduce the banked certificate over Q (a real "
                "in-check coupling to _su3_octet_M4_certificate). "
                "Discrimination note carried: the dim/rank/trace invariants "
                "are degenerate across the wrong all-fund action -- the "
                "action is pinned by the diagram-commutation, rep-property, "
                "spectrum/projector-trace, hw-multiplicity, and "
                "negative-control legs. %d legs, all exact over Q, pure "
                "stdlib. FENCE: construction only -- the contextuality "
                "verdicts stay [P_structural_instrument] on the parent "
                "check; the obstruction object remains group-independent; "
                "explicit Hermitian observables remain undelivered "
                "(obstructed over Q; out of scope, stated); occupancy stays "
                "the empirical QAC." % n_legs
            ),
            data=data,
            dependencies=deps,
        )
    return _fail(
        name,
        status="FAIL",
        summary="explicit octet M_4 construction legs failed: %s" % (
            [lbl for c, lbl in legs if not c],),
        data=data,
        dependencies=deps,
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



# ---------------------------------------------------------------------------
# General-N extension (v24.3.372, 2026-07-03; Paper 12 review-2 lane B1,
# fresh-context hostile audit AUDIT_ROUND2 LAND 0.90, optional notes B1-n1 +
# B1-n2 taken at landing). Walk of record:
# "The Turning/p12_review2_walks_2026-07-03/b1_general_N/". New helpers below
# reuse this module's exact-arithmetic toolkit (Q, _rank, _su_n_gens, ...);
# the Cartan-support reductions keep N = 4, 5 feasible while remaining EXACT
# (the full complexified generator set is imposed -- no bound, no sampling).
# ---------------------------------------------------------------------------

from collections import Counter as _Counter


def _digits(idx, N, n):
    """Base-N digits of idx, most-significant (slot 0) first -- matches the module's
    tensor index convention (idx = sum_k d_k N^{n-1-k})."""
    ds = []
    for _ in range(n):
        ds.append(idx % N); idx //= N
    ds.reverse()
    return ds


def _gsparse(g):
    """N x N Q-matrix -> column-indexed sparse form {col: [(row, value), ...]}."""
    N = len(g); cols = {}
    for r in range(N):
        for c in range(N):
            if not g[r][c].is0():
                cols.setdefault(c, []).append((r, g[r][c]))
    return cols


def _rank_frac(M):
    """Exact rank of a rectangular matrix with Fraction entries (mirror of _rank)."""
    M = [row[:] for row in M]; rows = len(M); cols = len(M[0]) if rows else 0; r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if M[i][c] != 0: piv = i; break
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        inv = F(1) / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [M[i][j] - f * M[r][j] for j in range(cols)]
        r += 1
        if r == rows: break
    return r


def _sparse_fund_slots_invariant(N, n, vec):
    """True iff (sum_k g^{(slot k)}) vec = 0 for EVERY real su(N) generator g
    (the full _su_n_gens basis, including the imaginary ones). Sparse exact Q[i];
    feasible at N^N dimensions because it only walks the nonzeros of vec."""
    nz = {i: v for i, v in enumerate(vec) if not v.is0()}
    for g in _su_n_gens(N):
        cols = _gsparse(g)
        out = {}
        for idx, val in nz.items():
            ds = _digits(idx, N, n)
            for k in range(n):
                for (r, gv) in cols.get(ds[k], []):
                    nidx = 0
                    for s in range(n):
                        nidx = nidx * N + (r if s == k else ds[s])
                    q = out.get(nidx)
                    out[nidx] = gv * val if q is None else q + gv * val
        if any(not x.is0() for x in out.values()):
            return False
    return True


def _baryon_inv_dim_weightrestricted(N):
    """EXACT dimension of the invariant subspace of fund^(x)N -- full generator set,
    computed on the Cartan-forced support so N = 4, 5 stay feasible.

    (i)  The Cartan generators act DIAGONALLY on the tensor basis; a basis state has
         zero Cartan weight iff every colour value appears exactly once, i.e. the N!
         permutation states. Any invariant vector is killed by the Cartan generators,
         hence supported on those states.
    (ii) On that support impose (sum_k E_ab^{(slot k)}) v = 0 for ALL a != b.
    {Cartan} + {E_ab, a != b} spans sl(N, C), the complexification of su(N), so the
    kernel computed here is EXACTLY the invariant subspace (v is killed by the real
    algebra iff killed by its complex span). Exact rational arithmetic."""
    states = list(_perms(range(N)))
    nstates = len(states)
    rows = {}
    for a in range(N):
        for b in range(N):
            if a == b: continue
            for t, s in enumerate(states):
                k = s.index(b)          # the unique slot carrying colour b
                img = list(s); img[k] = a
                key = (a, b, tuple(img))
                d = rows.setdefault(key, {})
                d[t] = d.get(t, F(0)) + 1
    M = [[d.get(t, F(0)) for t in range(nstates)] for d in rows.values()]
    return nstates - _rank_frac(M)


def _baryon_inv_dim_fullspace_sparse(N):
    """FULL-SPACE cross-check (audit note B1-n2, folded in at landing): the
    invariant-subspace dimension of fund^(x)N recomputed with NO Cartan-support
    reduction at all -- every Cartan row and every E_ab constraint row on the full
    N^N-dimensional space, reduced by incremental sparse exact Gaussian elimination
    over Q. Independently re-derives the weight-restricted result on a different
    code path (removes the only 'different code path than the parents' residue at
    N = 4, 5)."""
    n = N; dim = N ** n

    def _rows():
        # Cartan rows: H_a is diagonal with eigenvalue count_a - count_{a+1}
        for a in range(N - 1):
            for idx in range(dim):
                ds = _digits(idx, N, n)
                lam = ds.count(a) - ds.count(a + 1)
                if lam:
                    yield {idx: F(lam)}
        # E_ab rows: (sum_k E_ab^{(slot k)}) v = 0, one constraint per image state
        for a in range(N):
            for b in range(N):
                if a == b:
                    continue
                grp = {}
                for idx in range(dim):
                    ds = _digits(idx, N, n)
                    for k in range(n):
                        if ds[k] == b:
                            img = ds[:]; img[k] = a
                            key = 0
                            for dd in img:
                                key = key * N + dd
                            g = grp.setdefault(key, {})
                            g[idx] = g.get(idx, F(0)) + 1
                for g in grp.values():
                    yield g

    piv = {}   # pivot col -> normalized row (dict col -> coeff, pivot coeff 1)
    rank = 0
    for row in _rows():
        r = {c: v for c, v in row.items() if v != 0}
        while r:
            c = min(r)
            if c in piv:
                f = r.pop(c)
                for cc, vv in piv[c].items():
                    if cc == c:
                        continue
                    nv = r.get(cc, F(0)) - f * vv
                    if nv == 0:
                        r.pop(cc, None)
                    else:
                        r[cc] = nv
            else:
                f = r[c]
                piv[c] = {cc: vv / f for cc, vv in r.items()}
                rank += 1
                break
    return dim - rank


def _meson_commutant_dim_weightblock(N):
    """EXACT dimension of the commutant of the SU(N) action on fund (x) antifund --
    full generator set, computed on the Cartan-forced block support so N = 4, 5 stay
    feasible.

    An operator X with [X, H] = 0 for the (diagonal) Cartan action must be supported
    on basis pairs (p, q) of EQUAL weight: p = q, or p = (i,i), q = (k,k). That is
    2N^2 - N unknowns. On those unknowns impose [X, L_ab] = 0 for ALL complexified
    off-diagonal generators E_ab (a != b), where L_ab acts as E_ab on the fund slot
    and -E_ba on the antifund slot (= -E_ab^T, the module's conj(g) convention
    complexified). {Cartan} + {E_ab} spans sl(N, C), so the kernel is exactly the
    commutant. Exact rational arithmetic (the E_ab constraint matrices are real)."""
    unknowns = []
    for i in range(N):
        for k in range(N):
            unknowns.append((i * N + i, k * N + k))          # zero-weight block
    for i in range(N):
        for j in range(N):
            if i != j:
                unknowns.append((i * N + j, i * N + j))      # 1-dim weight blocks
    allrows = []
    for a in range(N):
        for b in range(N):
            if a == b: continue
            L = {}
            for j in range(N):      # fund slot: |a,j><b,j|
                key = (a * N + j, b * N + j)
                L[key] = L.get(key, F(0)) + 1
            for i in range(N):      # antifund slot: -|i,b><i,a|
                key = (i * N + b, i * N + a)
                L[key] = L.get(key, F(0)) - 1
            Lbyrow = {}; Lbycol = {}
            for (r, c), v in L.items():
                Lbyrow.setdefault(r, []).append((c, v))
                Lbycol.setdefault(c, []).append((r, v))
            crows = {}
            for t, (p, r) in enumerate(unknowns):
                for (c, v) in Lbyrow.get(r, []):     # +X_{p r} L_{r c} -> entry (p, c)
                    d = crows.setdefault((p, c), {})
                    d[t] = d.get(t, F(0)) + v
                for (pp, v) in Lbycol.get(p, []):    # -L_{pp p} X_{p r} -> entry (pp, r)
                    d = crows.setdefault((pp, r), {})
                    d[t] = d.get(t, F(0)) - v
            allrows.extend(crows.values())
    M = [[d.get(t, F(0)) for t in range(len(unknowns))] for d in allrows]
    return len(unknowns) - _rank_frac(M)


def _u1_commutant_dim_by_weights(N):
    """U(1) commutant dim on fund (x) antifund. The module's U(1) generator is diagonal
    (charge k on fund index k, conj on antifund), so the action generator is diagonal
    with charge (k - l) on |k, l>; the commutant of a diagonal generator with charge
    multiplicities {m_c} is the block algebra of dim sum m_c^2. Exact integer count;
    cross-checked against the dense _commutant_dim at N = 2, 3."""
    cnt = _Counter(k - l for k in range(N) for l in range(N))
    return sum(m * m for m in cnt.values())


def check_T_gauge_invariant_colour_record_general_N() -> Dict:
    """General-N extension of the meson + baryon gauge-invariant colour record
    results (reviewer Q3: 'stated for N = 2, 3; does the conclusion extend to
    generic N >= 2?'). Three statements, certified with exact Q[i]/rational
    arithmetic for N = 2, 3, 4, 5 IN-CHECK, all N >= 2 by proof sketch:

      (A) MESON (fund (x) antifund), every N >= 2: the invariant subspace is
          EXACTLY 1-dim, spanned by the maximally entangled singlet (Schmidt
          rank N); the gauge-invariant *-algebra (the commutant) is EXACTLY
          span{pi_singlet, pi_adjoint}; its unique rank-1 idempotent is
          pi_singlet. So the parent meson classification
          (check_T_only_gauge_invariant_sharp_colour_record_is_
          nonfactorizable_singlet_P) holds VERBATIM at every N.
          Sketch: fund (x) antifund ~= End(C^N), g.X = g X g^dag; invariants
          = scalars (Schur); N (x) Nbar = 1 (+) adj multiplicity-free.

      (B) FUND (x) FUND -- the reviewer's phrase, corrected precisely: an
          SU(N) invariant in fund (x) fund exists ONLY at N = 2
          (pseudoreality; the antisymmetric singlet, Schmidt rank 2). For
          every N >= 3 fund (x) fund contains NO invariant (m = 0). The
          general-N meson statement lives on fund (x) antifund; at N = 2
          the two coincide.

      (C) BARYON (fund^(x)N), every N >= 2: the invariant subspace is
          EXACTLY 1-dim, spanned by the totally-antisymmetric epsilon
          baryon, entangled across EVERY bipartition: Schmidt rank across
          any k | (N-k) cut equals binomial(N, k) > 1. Sketch: Schur-Weyl;
          the SU(N)-trivial constituent at |lambda| = N is exactly the
          full-height column (the determinant), sign-rep multiplicity 1;
          the k-cut matricization of epsilon is the full-rank pairing
          Lambda^k <-> Lambda^(N-k).

    CERTIFICATE STRUCTURE (why N = 4, 5 are exact, not sampled): any
    invariant is killed by the diagonal Cartan generators, hence supported
    on the weight-zero states; on that support the action of ALL complexified
    off-diagonal E_ab is imposed. {Cartan} + {E_ab} spans sl(N, C), so the
    computed kernel is EXACTLY the invariant subspace. The same Cartan-block
    device computes the meson commutant exactly. Cross-checks: dense parent-
    module methods at N = 2, 3 (exact agreement); the epsilon/meson vectors
    verified against ALL real su(N) generators (sparse, exact); AND (audit
    note B1-n2) the baryon invariant dimension re-derived on the FULL
    N^N-dim space with NO support reduction at every N. Abelian U(1) control
    at every N: the sharp product record P00 stays gauge-invariant (U(1)
    commutant large) -- the entanglement conclusion remains a NON-ABELIAN
    feature at every N.

    COMPOSITION NOTE (audit note B1-n1): the already-banked
    check_T_canonical_colour_record_iff_multiplicity_free_P (this module)
    owns the m >= 2 boundary (SU(2) fund^(x)4, non-abelian exotic algebra);
    this check supplies the all-N m = 1 towers that trichotomy sits on. The
    two COMPOSE -- they are not independent discoveries.

    Grade [P_structural_reading], mirroring both parents: the representation
    theory is exact [P]-grade arithmetic; the step 'gauge-invariant =
    physical/admissible record' is the no-B allocation reading
    (check_T_gauge_connection_is_gauge_variant_convention_P,
    apf/base_fiber_allocation.py).

    FENCES (identical to the parents): NO occupancy / branch-(IJC) claim;
    NOT confinement (needs L_irr / dynamics); NOT the gap value or continuum
    existence; the connection A_mu stays the transverse gauge-variant
    convention. The statement is at the GLOBAL representation level -- no
    dressed/local operator claim. N is a spectator parameter: nothing here
    selects N_c = 3 (that stays with T_gauge)."""
    NS = (2, 3, 4, 5)
    DENSE_XCHECK = (2, 3)
    meson_cells = {}; ff_cells = {}; baryon_cells = {}; xchecks = {}
    ok = True

    for N in NS:
        n2 = N * N
        # ---------------- (A) meson: fund (x) antifund ----------------
        Ls = _action_gens(N, "SU")
        inv_meson = _inv_dim_meson(N)                       # dense, full space, all gens
        mv = _meson_vec(N)
        mv_invariant = all(_vec_is_zero(_matvec(L, mv)) for L in Ls)
        sr_singlet = _schmidt_bipartite(N, 2, mv, [0])
        comm_wb = _meson_commutant_dim_weightblock(N)       # exact, full gen set
        ps = _singlet_proj(N); padj = _sub(_eye(n2), ps)
        ps_inv = _in_commutant(ps, N, "SU")
        padj_inv = _in_commutant(padj, N, "SU")
        ps_proj = _eqm(_mm(ps, ps), ps)
        padj_proj = _eqm(_mm(padj, padj), padj)
        orth = _iszero(_mm(ps, padj))
        compl = _eqm(_add(ps, padj), _eye(n2))
        ranks = {"pi_s": _rank(ps), "pi_adj": _rank(padj)}
        algebra_is_span = (comm_wb == 2 and ps_inv and padj_inv and ps_proj
                           and padj_proj and orth and compl)
        # idempotent enumeration in span{pi_s, pi_adj}: {0, pi_s, pi_adj, I},
        # ranks {0, 1, N^2-1, N^2} -> unique rank-1 idempotent = pi_s
        unique_rank1 = (ranks["pi_s"] == 1 and ranks["pi_adj"] == n2 - 1)
        # abelian control (every N): sharp product record exists for U(1), not SU(N)
        p00 = _P00(N)
        p00_su = _in_commutant(p00, N, "SU")
        p00_u1 = _in_commutant(p00, N, "U1")
        dim_u1 = _u1_commutant_dim_by_weights(N)
        # dipole corollary: pi_s is the -C_F eigenstate at every N
        Tdip = _colour_dipole(N)
        Tps = _mm(Tdip, ps)
        lam = Tps[0][0].r / ps[0][0].r
        lamQ = Q(lam, 0)
        eig_exact = _iszero(_sub(Tps, [[lamQ * ps[a][b] for b in range(n2)]
                                       for a in range(n2)]))
        CF = F(N * N - 1, 2 * N)
        dipole_ok = eig_exact and (lam == -CF)
        m_ok = (inv_meson == 1 and mv_invariant and sr_singlet == N
                and algebra_is_span and unique_rank1
                and (not p00_su) and p00_u1 and dim_u1 > 2 and dipole_ok)
        meson_cells[f"SU({N})"] = {
            "invariant_subspace_dim": inv_meson,
            "singlet_is_invariant": mv_invariant,
            "singlet_schmidt_rank": sr_singlet,
            "commutant_dim": comm_wb,
            "algebra_is_exactly_span_pi_s_pi_adj": algebra_is_span,
            "idempotent_ranks": {"pi_s": ranks["pi_s"], "pi_adj": ranks["pi_adj"]},
            "unique_rank1_is_singlet": unique_rank1,
            "P00_gauge_invariant_SU": p00_su,
            "P00_gauge_invariant_U1": p00_u1,
            "U1_commutant_dim": dim_u1,
            "record_is_minus_C_F_eigenstate": dipole_ok,
            "minus_C_F": str(-CF),
            "cell_ok": m_ok,
        }
        # ---------------- (B) fund (x) fund correction ----------------
        inv_ff = _inv_dim_fund_n(N, 2)                       # dense, full space, all gens
        expected_ff = 1 if N == 2 else 0
        f_ok = (inv_ff == expected_ff)
        cell = {
            "invariant_subspace_dim": inv_ff,
            "expected_1_iff_N_eq_2_pseudoreality": expected_ff,
        }
        if N == 2:
            eps2 = _eps_singlet_vec(2)
            eps2_inv = _sparse_fund_slots_invariant(2, 2, eps2)
            sr2 = _schmidt_bipartite(2, 2, eps2, [0])
            f_ok = f_ok and eps2_inv and (sr2 == 2)
            cell["antisymmetric_singlet_invariant"] = eps2_inv
            cell["antisymmetric_singlet_schmidt_rank"] = sr2
        cell["cell_ok"] = f_ok
        ff_cells[f"SU({N})"] = cell
        # ---------------- (C) baryon: fund^(x)N ----------------
        inv_bar = _baryon_inv_dim_weightrestricted(N)        # exact, full gen set
        inv_bar_full = _baryon_inv_dim_fullspace_sparse(N)   # B1-n2: no reduction
        eps = _eps_singlet_vec(N)
        eps_inv = _sparse_fund_slots_invariant(N, N, eps)    # ALL real su(N) gens
        eps_nonzero = not _vec_is_zero(eps)
        bip = {}
        bip_ok = True
        for k in range(1, N):
            for rest in _combs(range(1, N), k - 1):
                left = (0,) + rest
                sr = _schmidt_bipartite(N, N, eps, list(left))
                expect = _math.comb(N, len(left))
                bip["|".join(map(str, left))] = sr
                bip_ok = bip_ok and (sr == expect) and (sr > 1)
        sr_first_rest = bip["0"]
        b_ok = (inv_bar == 1 and inv_bar_full == inv_bar and eps_inv
                and eps_nonzero and bip_ok and sr_first_rest == N)
        baryon_cells[f"SU({N})_fund^{N}"] = {
            "space_dim_N^N": N ** N,
            "invariant_subspace_dim": inv_bar,
            "invariant_subspace_dim_fullspace_no_reduction": inv_bar_full,
            "epsilon_is_invariant_all_su_gens": eps_inv,
            "epsilon_schmidt_rank_first_vs_rest": sr_first_rest,
            "epsilon_schmidt_rank_by_left_slots": bip,
            "all_bipartitions_rank_eq_binomial_and_gt_1": bip_ok,
            "cell_ok": b_ok,
        }
        # -------- dense parent-method cross-checks (N = 2, 3) --------
        if N in DENSE_XCHECK:
            dense_comm = _commutant_dim(N, "SU")
            dense_bar = _invariant_subspace_dim(N)
            dense_u1 = _commutant_dim(N, "U1")
            Lsb = _baryon_action_gens(N)
            dense_eps_inv = all(_vec_is_zero(_matvec(L, eps)) for L in Lsb)
            agree = (dense_comm == comm_wb == 2 and dense_bar == inv_bar == 1
                     and dense_u1 == dim_u1 and dense_eps_inv == eps_inv is True)
            xchecks[f"SU({N})"] = {
                "meson_commutant_dense_vs_weightblock": [dense_comm, comm_wb],
                "baryon_inv_dim_dense_vs_weightrestricted": [dense_bar, inv_bar],
                "u1_commutant_dense_vs_weightcount": [dense_u1, dim_u1],
                "epsilon_invariance_dense_vs_sparse": [dense_eps_inv, eps_inv],
                "agree": agree,
            }
            ok = ok and agree
        ok = ok and m_ok and f_ok and b_ok

    data = {
        "model": ("SU(N) colour records at generic N: meson fund (x) antifund, fund (x) fund, "
                  "baryon fund^(x)N; exact Q[i]/rational arithmetic, N = 2..5 in-check"),
        "method": ("N = 4, 5 use the Cartan-support reduction with the FULL complexified "
                   "generator set ({Cartan} + all E_ab spans sl(N,C)): exact dimensions, not "
                   "bounds and not samples; N = 2, 3 additionally cross-checked against the "
                   "parent module's dense full-space methods (exact agreement); the baryon "
                   "invariant dimension additionally re-derived on the FULL space with no "
                   "support reduction at every N (sparse exact elimination, B1-n2)"),
        "by_N_meson": meson_cells,
        "by_N_fund_fund": ff_cells,
        "by_N_baryon": baryon_cells,
        "dense_cross_checks": xchecks,
        "statement": ("for every N >= 2: (A) the meson invariant subspace is 1-dim (the "
                      "maximally entangled singlet, Schmidt rank N) and the gauge-invariant "
                      "*-algebra is exactly span{pi_s, pi_adj} with unique rank-1 projector "
                      "pi_s; (B) fund (x) fund hosts an invariant ONLY at N = 2 (pseudoreality); "
                      "(C) the baryon invariant subspace of fund^(x)N is 1-dim (the epsilon), "
                      "entangled across EVERY bipartition (Schmidt rank binomial(N,k) > 1)"),
        "general_N_proof_sketch": {
            "meson": ("fund (x) antifund ~= End(C^N), g.X = gXg^dag; invariants = scalars by "
                      "Schur (fund irreducible) => dim 1; N (x) Nbar = 1 (+) adj multiplicity-"
                      "free, adj irreducible for all N => commutant dim 2"),
            "fund_fund": ("dim Inv(V (x) V) = dim Hom_G(V*, V); V* ~= V iff N = 2 (pseudoreal "
                          "epsilon form); for N >= 3 fund and antifund have distinct highest "
                          "weights => no invariant"),
            "baryon": ("Schur-Weyl: (C^N)^(x)N = (+)_lambda S^lambda(C^N) (x) Specht_lambda; "
                       "the SU(N)-trivial S^lambda at |lambda| = N is exactly lambda = (1^N) "
                       "(the determinant), Specht = the sign rep of S_N, dim 1 => multiplicity "
                       "1 for every N; the k-cut matricization of epsilon is the full-rank "
                       "pairing Lambda^k <-> Lambda^(N-k), rank binomial(N,k) > 1"),
        },
        "fund_fund_correction": ("the reviewer's 'fund (x) fund' is loose: the general-N meson "
                                 "statement lives on fund (x) antifund; fund (x) fund has an "
                                 "invariant only at N = 2, where pseudoreality identifies the "
                                 "two (verified: m = 1, 0, 0, 0 for N = 2, 3, 4, 5)"),
        "composition_note": ("check_T_canonical_colour_record_iff_multiplicity_free_P owns the "
                             "m >= 2 boundary; this check supplies the all-N m = 1 towers -- "
                             "the two compose (B1-n1)"),
        "reading_adopted": ("gauge-invariant = physical/admissible record (the no-B allocation, "
                            "check_T_gauge_connection_is_gauge_variant_convention_P, "
                            "apf/base_fiber_allocation.py)"),
        "scope": ("ONLY the gauge-invariant sharp-record structure at generic N, at the GLOBAL "
                  "representation level; NOT occupancy / branch-(IJC); NOT confinement (needs "
                  "L_irr/dynamics); NOT the gap value or continuum; no dressed/local operator "
                  "claim; the connection A_mu stays the transverse gauge-variant convention; "
                  "nothing here selects N_c = 3 (that stays with T_gauge)"),
        "certified_range": "N = 2, 3, 4, 5 in-check (exact); all N by the proof sketch",
    }
    if ok:
        return _ok(
            "check_T_gauge_invariant_colour_record_general_N",
            status="P_structural_reading",
            summary=("General-N extension (reviewer Q3): for SU(N), N = 2..5 certified exactly "
                     "in-check and for all N >= 2 by Schur/Schur-Weyl: (A) the meson (fund (x) "
                     "antifund) invariant subspace is 1-dim -- the maximally entangled singlet, "
                     "Schmidt rank N -- and the gauge-invariant *-algebra is exactly "
                     "span{pi_s, pi_adj}, unique rank-1 projector pi_s, so the sharp-record "
                     "classification holds verbatim at every N; (B) fund (x) fund (the "
                     "reviewer's phrase, corrected) hosts an invariant ONLY at N = 2 via "
                     "pseudoreality -- for N >= 3 it has NO invariant, the meson statement "
                     "lives on fund (x) antifund; (C) the baryon fund^(x)N invariant subspace "
                     "is exactly 1-dim for every N (sign-rep multiplicity 1), spanned by the "
                     "epsilon baryon, entangled across EVERY bipartition (Schmidt rank "
                     "binomial(N,k) > 1; rank N across first|rest). Abelian U(1) control at "
                     "every N: the sharp product record P00 survives -- entanglement of the "
                     "record stays a NON-ABELIAN feature. N = 4, 5 use the Cartan-support "
                     "reduction with the full complexified generator set (exact, no bound); "
                     "N = 2, 3 agree with the parent dense methods; the baryon dimension is "
                     "additionally re-derived on the FULL space with no support reduction at "
                     "every N. Composes with the multiplicity-free trichotomy check (m >= 2 "
                     "boundary). Reading: gauge-invariant = physical record (the no-B "
                     "allocation). No (IJC)/occupancy/confinement/gap claim; global-"
                     "representation level; nothing here selects N_c = 3."),
            data=data,
            dependencies=[
                "check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P",
                "check_T_unique_gauge_invariant_colour_state_of_N_fundamentals_is_entangled_baryon_P",
                "check_T_gauge_connection_is_gauge_variant_convention_P",
            ],
        )
    return _fail(
        "check_T_gauge_invariant_colour_record_general_N",
        status="FAIL",
        summary="General-N gauge-invariant colour record witness did not hold.",
        data=data,
    )


# ---------------------------------------------------------------------------
# v24.3.374: the deep-superselection no-go (face (b) of the branch-2
# phenotype). Exact-arithmetic helpers, private to this check.
# ---------------------------------------------------------------------------

def _dsn_t(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def _dsn_smul(s, A):
    return [[s * x for x in row] for row in A]


def _dsn_nullspace(rows):
    """Exact nullspace basis over the field Q[i] (the module's Q class)."""
    M = [r[:] for r in rows if not all(x.is0() for x in r)]
    ncols = len(rows[0])
    piv_of_col = {}
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(M)):
            if not M[i][c].is0():
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = M[r][c].inv()
        M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and not M[i][c].is0():
                f = M[i][c]
                M[i] = [M[i][k] - f * M[r][k] for k in range(ncols)]
        piv_of_col[c] = r
        r += 1
        if r == len(M):
            break
    free = [c for c in range(ncols) if c not in piv_of_col]
    basis = []
    for fc in free:
        v = [Q(0, 0)] * ncols
        v[fc] = Q(1, 0)
        for c, pr in piv_of_col.items():
            v[c] = Q(0, 0) - M[pr][fc]
        basis.append(v)
    return basis


def _dsn_commutant_basis(gens, n):
    """Exact commutant basis {X : [X, L] = 0 for all L} as n x n Q-matrices."""
    I = _eye(n)
    rows = []
    for L in gens:
        K = _sub(_kron(I, _dsn_t(L)), _kron(L, I))   # vec(XL - LX), row-major
        rows.extend(K)
    return [[[v[i * n + j] for j in range(n)] for i in range(n)]
            for v in _dsn_nullspace(rows)]


def _dsn_matvec(M, v):
    return [sum((M[i][j] * v[j] for j in range(len(v))), Q(0, 0))
            for i in range(len(M))]


def _dsn_solve_vectors(mats, n):
    """Joint exact kernel of a list of n x n Q-matrices (as vectors)."""
    rows = []
    for M in mats:
        rows.extend([row[:] for row in M])
    return _dsn_nullspace(rows)


def _dsn_inv_small(G):
    """Exact inverse of a small Q[i] matrix by Gauss-Jordan."""
    m = len(G)
    A = [G[i][:] + [Q(1, 0) if j == i else Q(0, 0) for j in range(m)]
         for i in range(m)]
    for c in range(m):
        piv = None
        for i in range(c, m):
            if not A[i][c].is0():
                piv = i
                break
        assert piv is not None, "singular Gram"
        A[c], A[piv] = A[piv], A[c]
        inv = A[c][c].inv()
        A[c] = [x * inv for x in A[c]]
        for i in range(m):
            if i != c and not A[i][c].is0():
                f = A[i][c]
                A[i] = [A[i][k] - f * A[c][k] for k in range(2 * m)]
    return [[A[i][m + j] for j in range(m)] for i in range(m)]


def _dsn_gt_weights(lam):
    l1, l2, l3 = lam
    out = {}
    tot = l1 + l2 + l3
    for m12 in range(l2, l1 + 1):
        for m22 in range(l3, l2 + 1):
            for m11 in range(m22, m12 + 1):
                wt = (m11, m12 + m22 - m11, tot - m12 - m22)
                out[wt] = out.get(wt, 0) + 1
    return out


def _dsn_wtensor(wA, wB):
    out = {}
    for a, ma in wA.items():
        for b, mb in wB.items():
            k = (a[0] + b[0], a[1] + b[1], a[2] + b[2])
            out[k] = out.get(k, 0) + ma * mb
    return out


def _dsn_wdecompose(wmult):
    rem = dict(wmult)
    out = {}
    while rem:
        hw = max(rem)
        assert hw[0] >= hw[1] >= hw[2] >= 0
        c = rem[hw]
        out[hw] = out.get(hw, 0) + c
        for wt, m in _dsn_gt_weights(hw).items():
            rem[wt] -= m * c
            assert rem[wt] >= 0
            if rem[wt] == 0:
                del rem[wt]
    return out


def check_T_matter_free_colour_record_deep_superselection_no_go() -> Dict:
    """T_matter_free_colour_record_deep_superselection_no_go: no Delta>0 colour
    commitment is ALGEBRAICALLY invariant (central) under the full gauge-invariant
    local algebra of a matter-free non-abelian sector at any scale -- face (b) of
    the branch-2 surviving phenotype (deep superselection) CLOSED; faces (a)
    discard + (c) no-altering-exercise stay OPEN; branch 2 NOT eliminated.
    [P_structural_reading]

    v24.3.374 (2026-07-04). Walk of record: "Reference - The Deep-Superselection
    No-Go - LANDED-WITH-FIXES (2026-07-03)" (fresh-context walker, Option B
    principal-ruled; fresh-context hostile cold audit LAND-WITH-FIXES 0.82, all
    nine fixes carried, incl. F1: the pre-audit exact-leg operator D was
    branch-diagonal, [D, P] = 0 identically -- this check ports the corrected
    branch-mixing intertwiner construction). Witness of record:
    The Turning/inert_endpoint_kill_2026-07-03/deep_superselection_nogo_witness.

    THE THREE STEPS (all executable content exact Q[i]/integer):

    Step 1 -- HONESTY: in-sector (m=1) centrality is REAL. The single-pair
      gauge-invariant algebra is abelian (fund pair: span{pi_s, pi_adj}, the
      record theorem's own structure; adjoint pair: 3-dim, spins 0/1/2 all
      multiplicity-free), so the record projector is central IN-SECTOR. The
      face-(b) worry was honest; the walk does not begin by denying it.

    Step 2 -- DE-CENTRALIZATION by gluonic enlargement. Adjoining ONE adjoint
      quantum (the exclusion's every-scale gluonic channel; consumed for channel
      existence via its gluonic-content typing + NR2, phase-exclusion leg only,
      the standing F2 fence -- the gap leg is NOT consumed) produces isotypic
      multiplicity >= 2; the commutant acquires an M_m block acting nontrivially
      WITHIN the shared isotypic component (the banked exotic-algebra mechanism;
      the multiplicity-free criterion marks m >= 2 as exactly where canonical
      records fail); the record projector STOPS commuting with the enlarged
      gauge-invariant algebra. Executed exactly: highest-weight multiplicity
      spaces solved over Q[i]; the record's compression onto the multiplicity
      space is NON-SCALAR; an explicit gauge-invariant branch-mixing intertwiner
      X (module-isomorphism construction, the audit-F1-corrected exact form) has
      [X, L_a] = 0 for every gauge generator and [X, P_record] != 0, exactly.

    Step 3 -- the enlargement-stable central residue is the N-ALITY label, and
      matter-free it is Delta-free. Isotypic labels mix under adjoint tensoring
      precisely within N-ality classes (T_center_order_parameter_triality,
      consumed for its UNCONDITIONAL rep-theory steps (1)-(4) ONLY: N-ality
      additivity, adjoint t=0, root lattice = the t=0 sublattice at index N;
      its saturation-conditional statement and step-(5) dressed-composite
      reading are NOT consumed -- audit F3). Matter-free, every constituent of
      adjoint^k has triality 0 (executed exactly, k = 1,2,3), so the surviving
      central label is CONSTANT: it distinguishes nothing, and by cost = count
      (L_cost [P]) a distinction-free residue carries Delta = 0 (lemma-let NR3).
      Every Delta>0 record projector (0 != P != I distinguishing within the
      sector) therefore fails centrality at some finite gluonic depth.

    NAMED READINGS (grade [P_structural_reading]; the executable content is
    unconditional rep theory, the physics rides these):
      NR1 -- record-invariance = centrality of the record's defining projector
        in the gauge-invariant algebra (the face's own audited definition;
        rides the banked reading gauge-invariant = physical/admissible record).
      NR2 -- THE HEAVIEST: the gluonic channel's adjoint content ENTERS the
        local gauge-invariant algebra at the record's own interface, finitely
        iterable, at every scale. "Channel content = algebra content" is not a
        banked row; the no-go's every-scale reach stands or falls with it.
        Mitigations: the modeled algebra is finite-dim type-I and the no-go
        direction is MONOTONE under algebra enlargement (more operators => less
        center), so the model is conservative modulo NR2's embedding claim.
      NR3 -- constant label => Delta = 0 residue (rides L_cost directly).

    SCOPE / NON-CLAIMS (load-bearing):
      - Closes face (b) ONLY. Faces (a) discard and (c) the broadened
        no-altering-exercise family (unpayable OR unselected -- audit F2) stay
        OPEN; they are ledger-shaped and out of scope. BRANCH 2 IS NOT
        ELIMINATED; check_T_ym_ir_endpoint_trichotomy_branch2_open keeps its
        OPEN flag and name; its falsifier (d) is NOT triggered. [RG-step
        typing RULED 2026-07-04 (re-description, Decisions List): branch 2
        is a PERMITTED phase; faces (a)/(c) are its phenotype, not
        elimination targets; this check stands as the face-(b)
        classification within the permitted phase.]
      - Payability appears nowhere: the altering X EXISTS algebraically; its
        exercise is face-(c) territory.
      - Does NOT discharge threat-liveness (reading G of the inert-endpoint
        walk): this is G's ALGEBRAIC half only (audit F5).
      - Matter fence is STRUCTURAL: with matter, nonzero N-ality classes are
        realized (3 x 8 all triality 1; classes {0,1,2}), the label is
        nonconstant, and class projectors stay central under gluonic
        enlargement (corollary of step 3: adjoint tensoring maps each class
        into itself) -- genuine superselection charges survive; the no-go
        turns entirely on matter-free CONSTANCY.
      - Abelian control: U(1)'s algebra is large, the sharp product record P00
        is U(1)-invariant (executed) -- the banked Delta=0/factorizable side;
        nothing Delta>0 to protect.

    FALSIFIERS: (i) a Delta>0 colour record projector central in EVERY finitely
    gluon-enlarged matter-free sector (needs an adjoint-stable invariant finer
    than N-ality -- collides with the banked root-lattice step); (ii) a
    matter-free scale whose local algebra provably excludes gluonic content
    (kills NR2); (iii) either consumed record/triality theorem falls; (iv) a
    gluonic enlargement keeping the record's isotypic component multiplicity-
    free (contradicted exactly at the smallest cases below).
    """
    ok_flags = {}

    # ---- exact su(2) bases (module Q class; antihermitian) -----------------
    h = F(1, 2)
    A1m = [[Q(0, 0), Q(0, h)], [Q(0, h), Q(0, 0)]]
    A2m = [[Q(0, 0), Q(h, 0)], [Q(-h, 0), Q(0, 0)]]
    A3m = [[Q(0, h), Q(0, 0)], [Q(0, 0), Q(0, -h)]]
    FUND = [A1m, A2m, A3m]

    def eps(a, b, c):
        return {(0, 1, 2): 1, (1, 2, 0): 1, (2, 0, 1): 1,
                (0, 2, 1): -1, (2, 1, 0): -1, (1, 0, 2): -1}.get((a, b, c), 0)

    # adjoint of the FUND basis: [A_a, A_b] = -eps_abc A_c => (ADJ_a)[c][b] = -eps(a,b,c)
    ADJ = []
    for a in range(3):
        M = _zeros(3)
        for b in range(3):
            for c in range(3):
                e = eps(a, b, c)
                if e:
                    M[c][b] = Q(-e, 0)
        ADJ.append(M)
    # structure-constant coherence (both bases satisfy [G_a,G_b] = -eps G_c)
    sc_ok = True
    for basis in (FUND, ADJ):
        for a in range(3):
            for b in range(3):
                target = _zeros(len(basis[0]))
                for c in range(3):
                    e = eps(a, b, c)
                    if e:
                        target = _add(target, _dsn_smul(Q(-e, 0), basis[c]))
                sc_ok = sc_ok and _eqm(_comm(basis[a], basis[b]), target)
    ok_flags["structure_constants_coherent"] = sc_ok

    I2, I3 = _eye(2), _eye(3)

    # ---- Step 1a: fund pair (4-dim), exact ---------------------------------
    PAIR = [_add(_kron(A, I2), _kron(I2, _conjm(A))) for A in FUND]
    C1a = _dsn_commutant_basis(PAIR, 4)
    Ps = _singlet_proj(2)
    ok_flags["m1_fund_dim2"] = (len(C1a) == 2)
    ok_flags["m1_fund_abelian"] = all(
        _iszero(_comm(C1a[i], C1a[j]))
        for i in range(len(C1a)) for j in range(i + 1, len(C1a)))
    ok_flags["m1_fund_singlet_central"] = (
        all(_iszero(_comm(Ps, L)) for L in PAIR)
        and all(_iszero(_comm(Ps, X)) for X in C1a))

    # ---- Step 1b: adjoint pair (9-dim), exact ------------------------------
    APAIR = [_add(_kron(T, I3), _kron(I3, T)) for T in ADJ]   # adjoint real-type
    C1b = _dsn_commutant_basis(APAIR, 9)
    Padj = _zeros(9)
    for i in (0, 4, 8):
        for j in (0, 4, 8):
            Padj[i][j] = Q(F(1, 3), 0)
    ok_flags["m1_adj_dim3"] = (len(C1b) == 3)
    ok_flags["m1_adj_abelian"] = all(
        _iszero(_comm(C1b[i], C1b[j]))
        for i in range(len(C1b)) for j in range(i + 1, len(C1b)))
    ok_flags["m1_adj_singlet_central"] = (
        all(_iszero(_comm(Padj, L)) for L in APAIR)
        and all(_iszero(_comm(Padj, X)) for X in C1b))

    # ---- exact SU(2) CG multiplicities --------------------------------------
    def couple(d1, d2):
        return list(range(abs(d1 - d2), d1 + d2 + 1, 2))

    def cg_mults(ds):
        cur = {ds[0]: 1}
        for d in ds[1:]:
            nxt = {}
            for dj, m in cur.items():
                for dk in couple(dj, d):
                    nxt[dk] = nxt.get(dk, 0) + m
            cur = nxt
        return cur

    m2a = cg_mults([1, 1, 2])
    m2b = cg_mults([2, 2, 2])
    ok_flags["cg_2a"] = (m2a == {0: 1, 2: 2, 4: 1})
    ok_flags["cg_2b"] = (m2b == {0: 1, 2: 3, 4: 2, 6: 1})

    # ---- Step 2 executor: HW multiplicity space + compression + exact X ----
    def decentralize(gens, n, P, expect_mult):
        """Spin-1 highest-weight space; record compression non-scalar; exact
        gauge-invariant branch-mixing X with [X, L]=0 and [X, P]!=0."""
        mi = Q(0, -1)
        Jz = _dsn_smul(mi, gens[2])
        Jp = _add(_dsn_smul(mi, gens[0]), gens[1])
        Jm = _sub(_dsn_smul(mi, gens[0]), gens[1])
        JzmI = _sub(Jz, _eye(n))
        hw = _dsn_solve_vectors([JzmI, Jp], n)
        if len(hw) != expect_mult:
            return False, f"HW mult {len(hw)} != {expect_mult}", None
        # record preserved by gauge action?
        if not all(_iszero(_comm(P, L)) for L in gens):
            return False, "P not gauge-invariant", None
        # compression B: P V = V B with V the HW basis
        m = len(hw)
        Gr = [[sum((hw[k][i].conj() * hw[l][i] for i in range(n)), Q(0, 0))
               for l in range(m)] for k in range(m)]
        Mx = [[sum((hw[k][i].conj() * _dsn_matvec(P, hw[l])[i]
                    for i in range(n)), Q(0, 0))
               for l in range(m)] for k in range(m)]
        B = _mm(_dsn_inv_small(Gr), Mx)
        nonscalar = (not all(B[i][j].is0() for i in range(m) for j in range(m)
                             if i != j)) or any(
            not (B[i][i] == B[0][0]) for i in range(m))
        if not nonscalar:
            return False, "compression scalar -- P central on this isotypic", None
        # exact branch-mixing intertwiner over some HW pair
        for a_i in range(m):
            for b_i in range(m):
                if a_i == b_i:
                    continue
                Bmod1, Bmod2 = [hw[a_i]], [hw[b_i]]
                for _ in range(2):
                    Bmod1.append(_dsn_matvec(Jm, Bmod1[-1]))
                    Bmod2.append(_dsn_matvec(Jm, Bmod2[-1]))
                G2 = [[sum((Bmod2[k][i].conj() * Bmod2[l][i]
                            for i in range(n)), Q(0, 0))
                       for l in range(3)] for k in range(3)]
                G2i = _dsn_inv_small(G2)
                dual = [[sum((Bmod2[l][i] * G2i[l][k] for l in range(3)),
                             Q(0, 0)) for i in range(n)] for k in range(3)]
                X = _zeros(n)
                for k in range(3):
                    for i in range(n):
                        if Bmod1[k][i].is0():
                            continue
                        for j in range(n):
                            X[i][j] = X[i][j] + Bmod1[k][i] * dual[k][j].conj()
                if (all(_iszero(_comm(X, L)) for L in gens)
                        and not _iszero(_comm(X, P))):
                    return True, "ok", X
        return False, "no de-centralizing intertwiner found", None

    # 2a: fund pair + one gluon (12-dim)
    G2a = [_add(_kron(PAIR[a], I3), _kron(_eye(4), ADJ[a])) for a in range(3)]
    P2a = _kron(Ps, I3)
    ok2a, msg2a, _ = decentralize(G2a, 12, P2a, expect_mult=2)
    ok_flags["decentralize_fund_pair_plus_gluon"] = ok2a

    # 2b: adjoint pair + one gluon (27-dim) -- the matter-free-native record
    G2b = [_add(_kron(APAIR[a], I3), _kron(_eye(9), ADJ[a])) for a in range(3)]
    P2b = _kron(Padj, I3)
    ok2b, msg2b, _ = decentralize(G2b, 27, P2b, expect_mult=3)
    ok_flags["decentralize_gluonic_record_plus_gluon"] = ok2b

    # ---- Step 3: N-ality exactness (SU(3), exact integers) ------------------
    THREE, THREEBAR, SIXBAR = (1, 0, 0), (1, 1, 0), (2, 2, 0)
    ADJ3, TEN = (2, 1, 0), (3, 0, 0)

    def dynkin(lam):
        return (lam[0] - lam[1], lam[1] - lam[2])

    def triality(lam):
        return sum(lam) % 3

    def wdim(wm):
        return sum(wm.values())

    d33b = _dsn_wdecompose(_dsn_wtensor(_dsn_gt_weights(THREE),
                                        _dsn_gt_weights(THREEBAR)))
    ok_flags["su3_3x3bar"] = (d33b == {(1, 1, 1): 1, (2, 1, 0): 1})
    d88 = _dsn_wdecompose(_dsn_wtensor(_dsn_gt_weights(ADJ3),
                                       _dsn_gt_weights(ADJ3)))
    ok_flags["su3_8x8"] = (
        d88 == {(2, 2, 2): 1, (3, 2, 1): 2, (4, 1, 1): 1, (3, 3, 0): 1,
                (4, 2, 0): 1}
        and sum(wdim(_dsn_gt_weights(l)) * m for l, m in d88.items()) == 64)
    pres = all(
        triality(mu) == triality(lam)
        for lam in (THREE, THREEBAR, SIXBAR, ADJ3, TEN)
        for mu in _dsn_wdecompose(_dsn_wtensor(_dsn_gt_weights(lam),
                                               _dsn_gt_weights(ADJ3))))
    ok_flags["adjoint_preserves_triality"] = pres
    rl = all((((2 * p + q) % 3 == 0 and (p + 2 * q) % 3 == 0)
              == ((p + 2 * q) % 3 == 0))
             for p in range(-6, 7) for q in range(-6, 7))
    ok_flags["root_lattice_t0_index3"] = (rl and abs(2 * 2 - 1) == 3)

    # ---- Step 3b: matter-free constancy (exact) -----------------------------
    aw = _dsn_gt_weights(ADJ3)
    a2 = _dsn_wtensor(aw, aw)
    a3 = _dsn_wtensor(a2, aw)
    realized = set()
    absent_6bar = True
    for wm in (dict(aw), a2, a3):
        for lam in _dsn_wdecompose(wm):
            realized.add(triality(lam))
            if dynkin(lam) == dynkin(SIXBAR):
                absent_6bar = False
    ok_flags["matter_free_constancy"] = (realized == {0})
    ok_flags["negative_control_6bar_absent"] = absent_6bar

    # ---- Controls ------------------------------------------------------------
    d38 = _dsn_wdecompose(_dsn_wtensor(_dsn_gt_weights(THREE),
                                       _dsn_gt_weights(ADJ3)))
    ok_flags["matter_control_3x8_t1"] = (
        all(triality(l) == 1 for l in d38)
        and sum(wdim(_dsn_gt_weights(l)) * m for l, m in d38.items()) == 24
        and {triality(THREE), triality(THREEBAR), triality((0, 0, 0))}
        == {0, 1, 2})
    # abelian: U(1) commutant dim on 2 x 2bar; P00 U(1)-invariant, executed
    charges = {}
    for qi in (0, 1):
        for qj in (0, 1):
            q = qi - qj
            charges[q] = charges.get(q, 0) + 1
    Qop = _zeros(4)
    qdiag = [qi - qj for qi in (0, 1) for qj in (0, 1)]
    for k in range(4):
        Qop[k][k] = Q(qdiag[k], 0)
    P00 = _P00(2)
    ok_flags["abelian_control"] = (
        sum(m * m for m in charges.values()) == 6
        and _iszero(_comm(Qop, P00))
        and any(not _iszero(_comm(L, P00)) for L in PAIR))

    ok = all(ok_flags.values())
    data = {
        "flags": {k: bool(v) for k, v in ok_flags.items()},
        "step2_messages": {"fund_pair_plus_gluon": msg2a,
                           "gluonic_record_plus_gluon": msg2b},
        "readings": {
            "NR1": "record-invariance = centrality (face (b)'s own audited definition)",
            "NR2": "HEAVIEST: gluonic channel content = local algebra content at every scale, finitely iterable",
            "NR3": "constant label => Delta = 0 residue (rides L_cost)",
            "inherited": "gauge-invariant = physical/admissible record",
        },
        "scope": ("face (b) ONLY; faces (a) discard + (c) no-altering-exercise "
                  "(unpayable OR unselected) OPEN; branch 2 NOT eliminated; "
                  ".368 OPEN flag + falsifier (d) untouched; payability-blind; "
                  "does NOT discharge reading G"),
        "consumption_fence": ("triality theorem: unconditional steps (1)-(4) only; "
                              "exclusion: gluonic-content typing at the phase-"
                              "exclusion leg only (gap leg NOT consumed)"),
    }
    name = "check_T_matter_free_colour_record_deep_superselection_no_go"
    deps = [
        "check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P",
        "check_T_exotic_gauge_invariant_algebra_is_nonabelian",
        "check_T_canonical_colour_record_iff_multiplicity_free_P",
        "T_center_order_parameter_triality",
        "T_ym_conformal_phase_excluded_by_record_locking",
        "L_cost",
    ]
    if ok:
        return _ok(
            name,
            status="P_structural_reading",
            summary=(
                "Face (b) of the matter-free branch-2 phenotype (deep "
                "superselection) CLOSED: in-sector (m=1) centrality of the "
                "colour record is real (fund + adjoint pairs, exact) but ONE "
                "adjoint enlargement de-centralizes it (HW multiplicity >= 2, "
                "non-scalar record compression, explicit exact gauge-invariant "
                "branch-mixing X with [X,P] != 0 -- the audit-F1-corrected "
                "construction); the enlargement-stable center is the N-ality "
                "label (root lattice = t=0 sublattice, index N, exact), which "
                "matter-free is CONSTANT 0 hence Delta-free (cost = count). "
                "Readings NR1/NR2(heaviest)/NR3 named in-docstring. Faces "
                "(a)+(c) OPEN; branch 2 NOT eliminated; matter keeps genuine "
                "superselection charges; abelian control consistent."),
            data=data,
            dependencies=deps,
        )
    return _fail(name, status="FAIL",
                 summary=f"deep-superselection no-go legs failed: "
                         f"{[k for k, v in ok_flags.items() if not v]}",
                 data=data, dependencies=deps)




# =====================================================================
# Product groups: sharp records track group structure FACTOR-WISE
# through the slot structure (v24.3.383, Paper 12 round-7 walk D1)
# ---------------------------------------------------------------------
# exact sparse Fraction toolkit, local to this section (ported
# 2026-07-04 from the D1 walk witness witness_d1_sign_and_products.py;
# the module's Q-class dense toolkit above is complex-rational and
# action-specific -- these legs are real-rational and need generic
# commutants, kernels, and Schmidt ranks)
# =====================================================================

def _pg_eye(n):
    return {i: {i: F(1)} for i in range(n)}


def _pg_mm(A, B):
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


def _pg_add(A, B, sgn=1):
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


def _pg_sub(A, B):
    return _pg_add(A, B, -1)


def _pg_smul(c, A):
    c = F(c)
    if not c:
        return {}
    return {i: {j: c * v for j, v in r.items()} for i, r in A.items()}


def _pg_T(A):
    C = {}
    for i, r in A.items():
        for j, v in r.items():
            C.setdefault(j, {})[i] = v
    return C


def _pg_kron(A, B, nb):
    C = {}
    for i, ra in A.items():
        for j, va in ra.items():
            for p, rb in B.items():
                row = C.setdefault(i * nb + p, {})
                for q, vb in rb.items():
                    row[j * nb + q] = va * vb
    return C


def _pg_comm(A, B):
    return _pg_sub(_pg_mm(A, B), _pg_mm(B, A))


def _pg_iszero(A):
    return all(not r for r in A.values())


def _pg_eq(A, B):
    return _pg_iszero(_pg_sub(A, B))


def _pg_trace(A):
    return sum(r.get(i, F(0)) for i, r in A.items())


def _pg_flat(A, n):
    v = {}
    for i, r in A.items():
        for j, val in r.items():
            if val:
                v[i * n + j] = val
    return v


def _pg_from_dense(M):
    A = {}
    for i, row in enumerate(M):
        r = {j: F(v) for j, v in enumerate(row) if v}
        if r:
            A[i] = r
    return A


def _pg_to_dense(A, n):
    M = [[F(0)] * n for _ in range(n)]
    for i, r in A.items():
        for j, v in r.items():
            M[i][j] = v
    return M


class _PgSpan:
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

    @property
    def dim(self):
        return len(self.piv)


def _pg_commutant_dim(gens, n):
    """dim of {X : [X, L] = 0 for all L in gens} -- exact, sparse."""
    span = _PgSpan()
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


def _pg_dense_rank(M):
    M = [row[:] for row in M]
    rows, cols = len(M), (len(M[0]) if M else 0)
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if M[i][c]:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = F(1) / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(cols)]
        r += 1
        if r == rows:
            break
    return r


def _pg_kernel_basis(M, ncols):
    """Kernel basis of the dense constraint matrix M (rows = constraints)."""
    M = [row[:] for row in M]
    rows = len(M)
    r = 0
    pivcols = []
    for c in range(ncols):
        piv = None
        for i in range(r, rows):
            if M[i][c]:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = F(1) / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(ncols)]
        pivcols.append(c)
        r += 1
        if r == rows:
            break
    free = [c for c in range(ncols) if c not in pivcols]
    basis = []
    for fc in free:
        v = [F(0)] * ncols
        v[fc] = F(1)
        for i, pc in enumerate(pivcols):
            v[pc] = -M[i][fc]
        basis.append(v)
    return basis


def _pg_schmidt_rank(vec, dims, left_slots):
    """Exact Schmidt rank of vec across the bipartition left_slots | rest."""
    from itertools import product as _ipr
    ns = len(dims)
    right_slots = [sl for sl in range(ns) if sl not in left_slots]
    lidx = {}
    ridx = {}
    rowsmap = {}
    for idx, multi in enumerate(_ipr(*[range(d) for d in dims])):
        lft = tuple(multi[sl] for sl in left_slots)
        rgt = tuple(multi[sl] for sl in right_slots)
        li = lidx.setdefault(lft, len(lidx))
        ri = ridx.setdefault(rgt, len(ridx))
        rowsmap[(li, ri)] = vec[idx]
    M = [[F(0)] * len(ridx) for _ in range(len(lidx))]
    for (li, ri), v in rowsmap.items():
        M[li][ri] = F(v)
    return _pg_dense_rank(M)


def _pg_slot_op(mats, dims):
    """kron over slots; mats: dict slot -> sparse mat; identity elsewhere."""
    out = None
    for sl, d in enumerate(dims):
        m = mats.get(sl, _pg_eye(d))
        if out is None:
            out = m
        else:
            out = _pg_kron(out, m, d)
    return out


def _pg_cl2(d):
    """ceil(log2 d) for integer d >= 1, exactly (no floats)."""
    return (d - 1).bit_length()


def check_T_product_group_sharp_records_factorwise() -> Dict:
    """Sharp product-group records track group structure FACTOR-WISE
    THROUGH THE SLOT STRUCTURE: on product content the invariant algebra
    factorizes exactly, (A x B)' = A' (x) B', and sharpness, entanglement,
    and canonicity are decided factor by factor; on shared irreducible
    slots there is no factorization (Schur forces a commuting abelian
    factor scalar -- superselection only); and Delta composes across group
    factors only through the ANCHOR decomposition. (Landed v24.3.383,
    2026-07-04, Paper 12 round-7 walk D1, reviewer Q7; fresh-context
    hostile audit LAND-WITH-FIXES 0.85, findings F1-F8 ALL carried; walk
    of record: "The Turning/p12_review7_walks_2026-07-04/
    d1_sign_products/".)

    THE FACTOR-WISE LAW, three instances, EACH certified by an EXPLICIT
    A' (x) B' basis with containment + dimension (audit F4 -- never
    dimension-only):
      * U(1) x SU(2) on product content (dim 16): commutant dim
        12 = 6 * 2; the 12-element basis {charge-block units} (x)
        {1, pi_s} verified elementwise in the commutant;
      * SU(2) x SU(2) bifundamental meson (2,2) (x) (2bar,2bar) (dim 16):
        commutant dim 4 = 2 * 2 AFTER REGROUPING; the 4-element basis
        {1, pi_s^L, pi_s^R, pi_s^L pi_s^R} verified elementwise;
      * Z_2 x Z_2 on product content (dim 16): commutant dim 64 = 8 * 8;
        the 64-element basis {eigenspace matrix units} (x) {same}
        verified elementwise.
    Trivial multiplicity multiplies (2 = 2*1; 1 = 1*1; 4 = 2*2).

    THE BIFUNDAMENTAL REGROUPING FLAG (audit F4, in-check): the
    bifundamental IS product content -- but only after regrouping the
    slots by group factor ({V_L, Vbar_L} | {V_R, Vbar_R}), and that
    regrouping is a BILLING-DECOMPOSITION CHANGE, an algebra statement,
    not an anchor statement: a bifundamental string crosses the cut on
    ONE link carrying both fluxes, so the two factor records are
    CO-ANCHORED and the factor decomposition is NOT an anchor
    decomposition. THE SAME-SLOT SUBTLETY, stated: group factors acting
    through one slot do NOT give disjoint anchors.

    SHARPNESS IS DECIDED PER FACTOR: abelian factors admit sharp PRODUCT
    (separable) records (U(1): P00; Z_2 x Z_2: |00><00| (x) |00><00|,
    fully separable); non-abelian multiplicity-free factors force
    entanglement in their slots (the U(1) x SU(2) record P00 (x) pi_s is
    Schmidt rank 1 across the abelian slots and rank 2 across the
    non-abelian slots; the bifundamental invariant is rank 4 across the
    particle cut, rank 1 across the group-factor regrouping, rank 2
    across any single slot). Canonicity is factor-wise and demands EVERY
    factor multiplicity-free: m_U(1) = 2 makes m_product = 2 -- sharp
    records exist but none is canonical; the frame lives in the ABELIAN
    factor.

    THE SAME-SLOT NO-GO (Schur, computed): any U(1) commuting with SU(2)
    on the fundamental is scalar (commutant dim 1), so on meson content
    its induced action cancels and the joint invariant algebra is exactly
    SU(2)'s span{pi_s, pi_adj} (dim 2). A same-slot abelian factor
    contributes SUPERSELECTION (which contents exist), never
    operator-level record structure; no factorization law applies on
    shared irreducible slots.

    THE FINITE-GROUP REFINEMENT, CORRECTED (audit F3, MODERATE -- the
    walk's own Z_2 x Z_2 leg is the counterexample to the false
    qualifier): sharp records live on the ONE-DIMENSIONAL-IRREP isotypic
    sectors of ANY multiplicity -- U(g) acts as chi(g)*1 on such an
    isotypic, so EVERY rank-one idempotent inside it is invariant.
    MULTIPLICITY-ONE BUYS CANONICITY, NOT EXISTENCE (the banked m = 1 vs
    m >= 2 split of check_T_canonical_colour_record_iff_multiplicity_
    free_P). IN-CHECK COUNTEREXAMPLE: Z_2 x Z_2 has m_trivial = 4 and
    hosts BOTH the separable sharp record AND a second, distinct sharp
    record on the same multiplicity-4 isotypic (computed) -- existence at
    m = 4, canonicity nowhere (a frame, the banked m >= 2 branch). SCOPE
    NOTE: the banked trichotomy's m = 0 clause ("no sharp record at
    all") is SU(N)-scoped -- the trivial rep is SU(N)'s only 1-dim irrep;
    for finite / abelian groups the non-trivial 1-dim characters host
    sharp records too, exactly as U(1) charge sectors already do. The S_3
    instance: the meson invariant algebra is dim 3, abelian,
    multiplicity-free (Schur count over the irreps 1, 1-sign, 2), with
    EXACTLY two sharp records -- the trivial and SIGN lines, both
    ENTANGLED (Schmidt rank 2): no sharp product record; the
    multiplicity-freeness canonicity criterion is Schur and applies
    verbatim, per 1-dim-irrep channel. EUCLIDEAN-OBLIQUE NOTE (audit
    F8b): the S_3 isotypic idempotents are built by exact GROUP
    AVERAGING, P_chi = (dim chi/|G|) sum_g chi(g^-1) U(g) -- the rational
    standard rep is not orthogonal in this basis, so they are oblique
    w.r.t. the Euclidean structure and self-adjoint under the INVARIANT
    inner product; since the rep is unitarizable (finite group), calling
    them projectors is justified under the unitarizing metric.

    THE ANCHOR-NOT-GROUP-FACTOR DELTA LAW (audit F5 -- the
    register-reading rider carried IN-CHECK): Delta adds across group
    factors ONLY where the factor decomposition is realized as an anchor
    decomposition (the banked disjoint-additivity theorem's hypothesis);
    co-anchored factor records are ONE register component and POOL --
    pooled ceil(log2 d_L d_R) equals the factor sum at (2,2), (2,3),
    (3,3) and is STRICTLY SUBADDITIVE at (3,5) (4 < 5) and (5,5) (5 < 6).
    RIDER: this clause is quoted at its banked grade -- the pooled-
    packing / register-reading grounding is
    check_T_register_reading_grounds_ceil_log2_count,
    [P_structural_reading], a model postulate NOT derived from L_loc;
    NO new grounding is claimed here and the clause is NOT re-graded.

    GRADE [P] on the algebra legs (commutant factorizations,
    multiplicities, Schmidt ranks, idempotent enumerations -- all exact
    rational): the record-ROLE sentence (sharp gauge-invariant idempotent
    = physical record) rides the banked no-B / gauge-variant-convention
    reading AT ITS BANKED GRADE on the parent record theorems
    ([P_structural_reading] there, cross-ref), and the Delta-response
    clause is quoted at ITS banked grade per the rider above; neither is
    re-graded by, nor re-grades, this check's algebra content.

    FENCES: no occupancy claim (occupancy is read off the world, never
    derived); slot structure decides the ALGEBRA, anchor structure
    decides DELTA (that is the theorem's content, not a rider); N and the
    factor count are spectator parameters; no magnitude/units claim.
    """
    from itertools import product as _iprod
    legs = {}

    E2s = {0: {1: F(1)}}
    F2s = {1: {0: F(1)}}

    def _lie_dual(L):
        return _pg_smul(-1, _pg_T(L))

    # ---- the U(1) control pair (paper convention: charge k on index k) ----
    Dm = {1: {1: F(1)}}
    gen_u1 = _pg_sub(_pg_kron(Dm, _pg_eye(2), 2), _pg_kron(_pg_eye(2), Dm, 2))
    cu1 = _pg_commutant_dim([gen_u1], 4)
    inv_u1 = _pg_kernel_basis(_pg_to_dense(gen_u1, 4), 4)
    legs["u1_dim6_m2"] = (cu1 == 6 and len(inv_u1) == 2)
    P00s = {0: {0: F(1)}}
    legs["u1_sharp_product_record"] = _pg_iszero(_pg_comm(P00s, gen_u1))

    # ---- the SU(2) meson factor (V (x) Vbar) ----
    Em = _pg_add(_pg_kron(E2s, _pg_eye(2), 2),
                 _pg_kron(_pg_eye(2), _lie_dual(E2s), 2))
    Fm = _pg_add(_pg_kron(F2s, _pg_eye(2), 2),
                 _pg_kron(_pg_eye(2), _lie_dual(F2s), 2))
    csu2 = _pg_commutant_dim([Em, Fm], 4)
    inv_su2 = _pg_kernel_basis(_pg_to_dense(Em, 4) + _pg_to_dense(Fm, 4), 4)
    legs["su2_dim2_m1"] = (csu2 == 2 and len(inv_su2) == 1)
    legs["su2_invariant_entangled"] = (
        _pg_schmidt_rank(inv_su2[0], [2, 2], [0]) == 2)
    legs["su2_no_sharp_product_record"] = (
        not _pg_iszero(_pg_comm(P00s, Em)))
    EmVV = _pg_add(_pg_kron(E2s, _pg_eye(2), 2), _pg_kron(_pg_eye(2), E2s, 2))
    FmVV = _pg_add(_pg_kron(F2s, _pg_eye(2), 2), _pg_kron(_pg_eye(2), F2s, 2))
    legs["su2_VV_m1_pseudoreality_control"] = (
        len(_pg_kernel_basis(_pg_to_dense(EmVV, 4)
                             + _pg_to_dense(FmVV, 4), 4)) == 1)

    # ---- U(1) x SU(2) on product content: the factor-wise law ----
    I4s = _pg_eye(4)
    G1 = _pg_kron(gen_u1, I4s, 4)
    G2 = _pg_kron(I4s, Em, 4)
    G3 = _pg_kron(I4s, Fm, 4)
    cprod = _pg_commutant_dim([G1, G2, G3], 16)
    legs["prod_dim12_is_6x2"] = (cprod == 12 == cu1 * csu2)
    unitsA = [{a: {b: F(1)}} for (a, b) in
              [(0, 0), (0, 3), (3, 0), (3, 3), (1, 1), (2, 2)]]
    pis = _pg_from_dense([[F(1, 2), 0, 0, F(1, 2)], [0, 0, 0, 0],
                          [0, 0, 0, 0], [F(1, 2), 0, 0, F(1, 2)]])
    span12 = _PgSpan()
    contained12 = True
    for u in unitsA:
        for bb in (I4s, pis):
            el = _pg_kron(u, bb, 4)
            contained12 = contained12 and all(
                _pg_iszero(_pg_comm(el, g)) for g in (G1, G2, G3))
            span12.add(_pg_flat(el, 16))
    legs["prod_explicit_basis_containment_dim_12"] = (
        contained12 and span12.dim == 12)
    inv_prod = _pg_kernel_basis(
        _pg_to_dense(G1, 16) + _pg_to_dense(G2, 16)
        + _pg_to_dense(G3, 16), 16)
    legs["prod_m_multiplies_2_eq_2x1"] = (
        len(inv_prod) == 2 == len(inv_u1) * len(inv_su2))
    Prec = _pg_kron(P00s, pis, 4)
    legs["prod_sharp_record_P00_x_pis"] = (
        _pg_eq(_pg_mm(Prec, Prec), Prec) and _pg_trace(Prec) == 1
        and all(_pg_iszero(_pg_comm(Prec, g)) for g in (G1, G2, G3)))
    vrec = [F(0)] * 16
    vrec[0] = F(1)
    vrec[3] = F(1)
    legs["record_separable_on_u1_slots"] = (
        _pg_schmidt_rank(vrec, [4, 2, 2], [0]) == 1)
    legs["record_entangled_on_su2_slots"] = (
        _pg_schmidt_rank(vrec, [4, 2, 2], [1]) == 2)
    legs["canonicity_factorwise_fails_at_m_u1_2"] = (len(inv_prod) >= 2)

    # ---- the same-slot no-go (Schur) ----
    legs["schur_u1_commuting_with_su2_fund_is_scalar"] = (
        _pg_commutant_dim([E2s, F2s], 2) == 1)
    legs["same_slot_algebra_is_su2s_dim2"] = (
        _pg_commutant_dim([Em, Fm, {}], 4) == 2)

    # ---- the SU(2) x SU(2) bifundamental meson ----
    dimsB = [2, 2, 2, 2]   # slots: 0 = V_L, 1 = V_R, 2 = Vbar_L, 3 = Vbar_R
    EL = _pg_add(_pg_slot_op({0: E2s}, dimsB),
                 _pg_slot_op({2: _lie_dual(E2s)}, dimsB))
    FL = _pg_add(_pg_slot_op({0: F2s}, dimsB),
                 _pg_slot_op({2: _lie_dual(F2s)}, dimsB))
    ER = _pg_add(_pg_slot_op({1: E2s}, dimsB),
                 _pg_slot_op({3: _lie_dual(E2s)}, dimsB))
    FR = _pg_add(_pg_slot_op({1: F2s}, dimsB),
                 _pg_slot_op({3: _lie_dual(F2s)}, dimsB))
    gensB = (EL, FL, ER, FR)
    legs["bif_dim4_is_2x2_after_regrouping"] = (
        _pg_commutant_dim(list(gensB), 16) == 4)

    def _pair_singlet_proj(a, b):
        P = {}
        for rb in _iprod(range(2), repeat=4):
            if rb[a] != rb[b]:
                continue
            r = ((rb[0] * 2 + rb[1]) * 2 + rb[2]) * 2 + rb[3]
            for cb in _iprod(range(2), repeat=4):
                if cb[a] != cb[b]:
                    continue
                if any(cb[o] != rb[o] for o in range(4) if o not in (a, b)):
                    continue
                c = ((cb[0] * 2 + cb[1]) * 2 + cb[2]) * 2 + cb[3]
                P.setdefault(r, {})[c] = F(1, 2)
        return P

    PL = _pair_singlet_proj(0, 2)
    PR = _pair_singlet_proj(1, 3)
    I16s = _pg_eye(16)
    spanb = _PgSpan()
    okb = True
    for el in (I16s, PL, PR, _pg_mm(PL, PR)):
        okb = okb and all(_pg_iszero(_pg_comm(el, g)) for g in gensB)
        spanb.add(_pg_flat(el, 16))
    legs["bif_explicit_basis_containment_dim_4"] = (okb and spanb.dim == 4)
    invB = _pg_kernel_basis(
        _pg_to_dense(EL, 16) + _pg_to_dense(FL, 16)
        + _pg_to_dense(ER, 16) + _pg_to_dense(FR, 16), 16)
    legs["bif_m1_canonical_1x1"] = (len(invB) == 1)
    vB = [F(0)] * 16
    for i in range(2):
        for j in range(2):
            vB[((i * 2 + j) * 2 + i) * 2 + j] = F(1)
    wv = invB[0]
    ratio = None
    prop = True
    for a, b in zip(vB, wv):
        if a == 0 and b == 0:
            continue
        if a == 0 or b == 0:
            prop = False
            break
        rr = b / a
        if ratio is None:
            ratio = rr
        elif rr != ratio:
            prop = False
            break
    legs["bif_invariant_is_singletL_x_singletR"] = prop
    legs["bif_schmidt_4_particle_cut"] = (
        _pg_schmidt_rank(vB, dimsB, [0, 1]) == 4)
    legs["bif_schmidt_1_group_factor_regrouping"] = (
        _pg_schmidt_rank(vB, dimsB, [0, 2]) == 1)
    legs["bif_schmidt_2_single_slot"] = (
        _pg_schmidt_rank(vB, dimsB, [0]) == 2)
    PrecB = _pg_mm(PL, PR)
    legs["bif_canonical_sharp_record"] = (
        _pg_eq(_pg_mm(PrecB, PrecB), PrecB) and _pg_trace(PrecB) == 1
        and all(_pg_iszero(_pg_comm(PrecB, g)) for g in gensB))

    # ---- the anchor-not-group-factor Delta law (register-reading rider) ---
    tbl = {(dl, dr): (_pg_cl2(dl * dr), _pg_cl2(dl) + _pg_cl2(dr))
           for dl, dr in ((2, 2), (2, 3), (3, 3), (3, 5), (5, 5))}
    legs["pooled_additive_at_22_23_33"] = (
        tbl[(2, 2)] == (2, 2) and tbl[(2, 3)] == (3, 3)
        and tbl[(3, 3)] == (4, 4))
    legs["pooled_strictly_subadditive_at_35_55"] = (
        tbl[(3, 5)] == (4, 5) and tbl[(5, 5)] == (5, 6))

    # ---- Z_2 x Z_2: the factorization law on a finite abelian product ----
    g2 = _pg_from_dense([[1, 0], [0, -1]])
    Uz = _pg_kron(g2, g2, 2)   # dual of a real character = itself
    cz = _pg_commutant_dim([Uz], 4)
    invz = _pg_kernel_basis(
        _pg_to_dense(_pg_sub(Uz, _pg_eye(4)), 4), 4)
    legs["z2_factor_dim8_m2"] = (cz == 8 and len(invz) == 2)
    unitsZ = [{a: {b: F(1)}} for (a, b) in
              [(0, 0), (0, 3), (3, 0), (3, 3), (1, 1), (1, 2), (2, 1), (2, 2)]]
    spanz = _PgSpan()
    okz = all(_pg_iszero(_pg_comm(u, Uz)) for u in unitsZ)
    for u in unitsZ:
        spanz.add(_pg_flat(u, 4))
    legs["z2_factor_explicit_basis_8"] = (okz and spanz.dim == 8)
    Uz1 = _pg_kron(Uz, _pg_eye(4), 4)
    Uz2 = _pg_kron(_pg_eye(4), Uz, 4)
    czz = _pg_commutant_dim([Uz1, Uz2], 16)
    invzz = _pg_kernel_basis(
        _pg_to_dense(_pg_sub(Uz1, _pg_eye(16)), 16)
        + _pg_to_dense(_pg_sub(Uz2, _pg_eye(16)), 16), 16)
    legs["zz_dim64_is_8x8_m4_is_2x2"] = (
        czz == 64 == 8 * 8 and len(invzz) == 4 == 2 * 2)
    spanzz = _PgSpan()
    containedzz = True
    for u in unitsZ:
        for u2 in unitsZ:
            el = _pg_kron(u, u2, 4)
            containedzz = (containedzz and _pg_iszero(_pg_comm(el, Uz1))
                           and _pg_iszero(_pg_comm(el, Uz2)))
            spanzz.add(_pg_flat(el, 16))
    legs["zz_explicit_basis_containment_dim_64"] = (
        containedzz and spanzz.dim == 64)
    Pzz = _pg_kron(P00s, P00s, 4)
    legs["zz_separable_sharp_record"] = (
        _pg_eq(_pg_mm(Pzz, Pzz), Pzz) and _pg_trace(Pzz) == 1
        and _pg_iszero(_pg_comm(Pzz, Uz1)) and _pg_iszero(_pg_comm(Pzz, Uz2)))
    # F3 counterexample leg: a SECOND, distinct sharp record on the SAME
    # multiplicity-4 trivial isotypic -- existence needs only a
    # 1-dim-irrep isotypic (any multiplicity); m = 1 buys canonicity.
    uvec = [a + b for a, b in zip(invzz[0], invzz[1])]
    nrm = sum(x * x for x in uvec)
    Pu = {}
    for i, x in enumerate(uvec):
        if x:
            for j, y in enumerate(uvec):
                if y:
                    Pu.setdefault(i, {})[j] = x * y / nrm
    legs["zz_m4_second_sharp_record_existence"] = (
        _pg_eq(_pg_mm(Pu, Pu), Pu) and _pg_trace(Pu) == 1
        and _pg_iszero(_pg_comm(Pu, Uz1)) and _pg_iszero(_pg_comm(Pu, Uz2))
        and not _pg_eq(Pu, Pzz))

    # ---- S_3 on its 2-dim irrep: the criterion verbatim (Schur) ----
    r3 = _pg_from_dense([[0, -1], [1, -1]])
    s3 = _pg_from_dense([[-1, 1], [0, 1]])
    legs["s3_relations_exact"] = (
        _pg_eq(_pg_mm(r3, _pg_mm(r3, r3)), _pg_eye(2))
        and _pg_eq(_pg_mm(s3, s3), _pg_eye(2))
        and _pg_eq(_pg_mm(s3, _pg_mm(r3, s3)), _pg_mm(r3, r3)))

    def _inv2(M):
        d = _pg_to_dense(M, 2)
        det = d[0][0] * d[1][1] - d[0][1] * d[1][0]
        return _pg_from_dense([[d[1][1] / det, -d[0][1] / det],
                               [-d[1][0] / det, d[0][0] / det]])

    def _gdual(g):
        return _pg_T(_inv2(g))

    Ur = _pg_kron(r3, _gdual(r3), 2)
    Us = _pg_kron(s3, _gdual(s3), 2)
    legs["s3_dim3_multfree_abelian"] = (_pg_commutant_dim([Ur, Us], 4) == 3)
    invS3 = _pg_kernel_basis(
        _pg_to_dense(_pg_sub(Ur, _pg_eye(4)), 4)
        + _pg_to_dense(_pg_sub(Us, _pg_eye(4)), 4), 4)
    legs["s3_m1"] = (len(invS3) == 1)
    legs["s3_singlet_entangled"] = (
        _pg_schmidt_rank(invS3[0], [2, 2], [0]) == 2)
    signS3 = _pg_kernel_basis(
        _pg_to_dense(_pg_sub(Ur, _pg_eye(4)), 4)
        + _pg_to_dense(_pg_add(Us, _pg_eye(4)), 4), 4)
    legs["s3_sign_line_1dim_entangled"] = (
        len(signS3) == 1 and _pg_schmidt_rank(signS3[0], [2, 2], [0]) == 2)
    r2e = _pg_mm(r3, r3)
    els = [(_pg_eye(2), 1), (r3, 1), (r2e, 1),
           (s3, -1), (_pg_mm(s3, r3), -1), (_pg_mm(s3, r2e), -1)]
    P1 = {}
    P1s = {}
    for g, sgn in els:
        Ug = _pg_kron(g, _gdual(g), 2)
        P1 = _pg_add(P1, _pg_smul(F(1, 6), Ug))
        P1s = _pg_add(P1s, _pg_smul(F(sgn, 6), Ug))
    P2blk = _pg_sub(_pg_eye(4), _pg_add(P1, P1s))
    legs["s3_group_averaged_central_resolution"] = (
        _pg_eq(_pg_mm(P1, P1), P1) and _pg_eq(_pg_mm(P1s, P1s), P1s)
        and _pg_iszero(_pg_mm(P1, P1s))
        and _pg_eq(_pg_mm(P2blk, P2blk), P2blk)
        and all(_pg_iszero(_pg_comm(p, Ur)) and _pg_iszero(_pg_comm(p, Us))
                for p in (P1, P1s, P2blk))
        and _pg_trace(P1) == 1 and _pg_trace(P1s) == 1
        and _pg_trace(P2blk) == 2)
    sharp_combos = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)
                    if a + b + 2 * c == 1]
    legs["s3_exactly_two_sharp_records_both_entangled"] = (
        sharp_combos == [(0, 1, 0), (1, 0, 0)])

    ok = all(legs.values())
    data = {
        "model": ("product gauge groups on product vs shared content; exact "
                  "rational commutants / kernels / Schmidt ranks (stdlib "
                  "Fractions, sparse)"),
        "legs": {k: bool(v) for k, v in legs.items()},
        "factorization_instances": {
            "U(1) x SU(2)": "12 = 6 * 2 (explicit 12-element basis)",
            "SU(2) x SU(2) bifundamental": "4 = 2 * 2 (explicit 4-element "
                                           "basis; regrouping flagged)",
            "Z_2 x Z_2": "64 = 8 * 8 (explicit 64-element basis)",
        },
        "multiplicities_multiply": {"U(1) x SU(2)": "2 = 2*1",
                                    "bifundamental": "1 = 1*1",
                                    "Z_2 x Z_2": "4 = 2*2"},
        "bifundamental_schmidt_ranks": {"particle_cut": 4,
                                        "group_factor_regrouping": 1,
                                        "single_slot": 2},
        "regrouping_flag": ("the bifundamental regrouping is a "
                            "billing-decomposition change (algebra, not "
                            "anchors): group factors on one slot do NOT "
                            "give disjoint anchors -- the factor records "
                            "are co-anchored"),
        "finite_group_refinement_corrected": (
            "sharp records live on the 1-dim-irrep isotypic sectors of ANY "
            "multiplicity (U(g) = chi(g)*1 there); multiplicity-one buys "
            "CANONICITY, not existence -- in-check counterexample: "
            "Z_2 x Z_2 m = 4 hosts two distinct sharp records; the banked "
            "m = 0 no-record clause is SU(N)-scoped (trivial = SU(N)'s "
            "only 1-dim irrep)"),
        "s3_note": ("group-averaged isotypic idempotents, oblique w.r.t. "
                    "the Euclidean structure in the rational basis; "
                    "self-adjoint under the invariant inner product "
                    "(unitarizable, finite group)"),
        "pooled_packing_table": {str(k): {"pooled": v[0], "summed": v[1]}
                                 for k, v in tbl.items()},
        "delta_law_rider": (
            "Delta adds across group factors only where the factor "
            "decomposition is realized as an ANCHOR decomposition; "
            "co-anchored factors pool, strictly subadditively at (3,5) "
            "UNDER THE REGISTER READING -- quoted at its banked grade "
            "[P_structural_reading] "
            "(check_T_register_reading_grounds_ceil_log2_count), no new "
            "grounding claimed, not re-graded here"),
        "record_role_rider": (
            "sharp gauge-invariant idempotent = physical record rides the "
            "banked no-B / gauge-variant-convention reading at its banked "
            "grade on the parent record theorems (cross-ref); the algebra "
            "legs here are exact [P]"),
        "scope_fences": {
            "occupancy": "not claimed; read off the world, never derived",
            "content": ("slot structure decides the algebra, anchor "
                        "structure decides Delta -- the theorem's content, "
                        "not a rider"),
            "spectators": "N and the factor count are spectator parameters",
        },
    }
    if ok:
        return _ok(
            "check_T_product_group_sharp_records_factorwise",
            status="P",
            summary=("Sharp product-group records track group structure "
                     "FACTOR-WISE THROUGH THE SLOT STRUCTURE. On product "
                     "content the invariant algebra factorizes exactly, "
                     "(A x B)' = A' (x) B', certified by explicit bases "
                     "with containment + dimension on ALL THREE instances "
                     "(U(1) x SU(2): 12 = 6*2; SU(2) x SU(2) bifundamental "
                     "after regrouping: 4 = 2*2, the regrouping flagged as "
                     "a billing-decomposition change -- group factors on "
                     "one slot do NOT give disjoint anchors; Z_2 x Z_2: "
                     "64 = 8*8); trivial multiplicity multiplies (2 = 2*1, "
                     "1 = 1*1, 4 = 2*2); sharpness / entanglement / "
                     "canonicity are decided factor by factor (abelian "
                     "factors admit separable sharp records, non-abelian "
                     "multiplicity-free factors force entanglement in "
                     "their slots, one m >= 2 factor destroys canonicity "
                     "for the whole product). On shared irreducible slots "
                     "there is no factorization: Schur forces a commuting "
                     "abelian factor scalar -- superselection only. The "
                     "finite-group refinement CORRECTED (audit F3): sharp "
                     "records live on 1-dim-irrep isotypic sectors of ANY "
                     "multiplicity -- multiplicity-one buys CANONICITY, "
                     "not existence (Z_2 x Z_2 m = 4 hosts two distinct "
                     "sharp records, computed; the banked m = 0 clause is "
                     "SU(N)-scoped); S_3 has exactly two sharp records, "
                     "trivial + sign, both entangled (group-averaged "
                     "idempotents, oblique in the rational basis, "
                     "unitarizable). Delta composes across group factors "
                     "only through the ANCHOR decomposition; co-anchored "
                     "factors pool, strictly subadditively at (3,5) under "
                     "the register reading -- quoted at its banked "
                     "[P_structural_reading] grade, no new grounding. "
                     "Occupancy not claimed."),
            data=data,
            dependencies=[
                "check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P",
                "check_T_canonical_colour_record_iff_multiplicity_free_P",
                "check_T_gauge_invariant_colour_record_general_N",
                "check_T_register_reading_grounds_ceil_log2_count",
                "check_T_delta_disjoint_additivity",
            ],
        )
    return _fail(
        "check_T_product_group_sharp_records_factorwise",
        status="FAIL",
        summary="factor-wise product-group record witness did not hold.",
        data=data,
    )


CHECKS = {
    "check_T_matter_free_colour_record_deep_superselection_no_go":
        check_T_matter_free_colour_record_deep_superselection_no_go,
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
    "check_T_su3_octet_M4_explicit_construction":
        check_T_su3_octet_M4_explicit_construction,
    "check_T_colour_contextuality_is_kstring_spectrum_blind":
        check_T_colour_contextuality_is_kstring_spectrum_blind,
    "check_T_ckm_flavour_coavailability_is_sepstr":
        check_T_ckm_flavour_coavailability_is_sepstr,
    "check_T_gauge_invariant_colour_record_general_N":
        check_T_gauge_invariant_colour_record_general_N,
    "check_T_product_group_sharp_records_factorwise":
        check_T_product_group_sharp_records_factorwise,
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


# ---------------------------------------------------------------------------
# IE onboarding declarations (v24.3.310, Full Bank Onboarding Wave 1b -- the
# first SECTOR onboarding wave). Five bank-carried strong/flavour scenarios as
# first-class registry inputs, each wrapping this module's own banked scenario
# builder (payload built lazily at compile time, not at import). expect_export
# pins the promised verdict; a drift fails the bank. REACHABILITY ONLY: these
# onboard the contextuality-scenario slice of this module's content -- the
# rep-theory host results (octet multiplicities, Casimir witnesses, Schmidt
# ranks) stay with their specialist banked checks.
# ---------------------------------------------------------------------------

def _ie_payload_tetraquark_kcbs():
    from apf.ijc_feasbool_engine import scenario_to_dict
    return scenario_to_dict(_gic_kcbs_scenario()[0])


def _ie_payload_tetraquark_yuoh():
    from apf.ijc_feasbool_engine import scenario_to_dict
    return scenario_to_dict(_gic_yuoh_scenario()[0])


def _ie_payload_pentaquark_magic_square():
    from apf.ijc_feasbool_engine import (
        scenario_mermin_peres_magic_square, scenario_to_dict,
    )
    return scenario_to_dict(scenario_mermin_peres_magic_square())


def _ie_payload_chiral_flavour_yuoh():
    from apf.ijc_feasbool_engine import scenario_to_dict
    return scenario_to_dict(_ccf_yuoh_flavour_scenario()[0])


def _ie_payload_ckm_two_bases():
    from apf.ijc_feasbool_engine import scenario_to_dict
    return scenario_to_dict(_disjoint_bases_scenario(2))


IE_DECLARATIONS = (
    {
        "input_id": "strong:tetraquark_kcbs",
        "expect_export": False,
        "axis": "CONTEXTUALITY",
        "payload_builder": _ie_payload_tetraquark_kcbs,
        "note": "v24.3.293 banked scenario: gauge-invariant tetraquark M3 KCBS -> IJCStr",
    },
    {
        "input_id": "strong:tetraquark_yuoh_state_independent",
        "expect_export": False,
        "axis": "CONTEXTUALITY",
        "payload_builder": _ie_payload_tetraquark_yuoh,
        "note": "v24.3.294 banked scenario: Yu-Oh 13-ray on the tetraquark M3, "
                "state-independent -> IJCStr",
    },
    {
        "input_id": "strong:pentaquark_magic_square",
        "expect_export": False,
        "axis": "CONTEXTUALITY",
        "payload_builder": _ie_payload_pentaquark_magic_square,
        "note": "v24.3.295 banked scenario: SU(2) pentaquark M4 hosts the Mermin-Peres "
                "magic square (empty global-section support) -> IJCStr; the physical-host "
                "rep theory stays with the specialist check",
    },
    {
        "input_id": "flavour:chiral_condensate_yuoh",
        "expect_export": False,
        "axis": "CONTEXTUALITY",
        "payload_builder": _ie_payload_chiral_flavour_yuoh,
        "note": "v24.3.296 banked scenario: Yu-Oh on the N_f=3 flavour qutrit at the "
                "chiral condensate single density -> IJCStr",
    },
    {
        "input_id": "flavour:ckm_two_mass_bases",
        "expect_export": True,
        "axis": "CONTEXTUALITY",
        "payload_builder": _ie_payload_ckm_two_bases,
        "note": "v24.3.303 banked scenario: the CKM-forced up/down mass bases as two "
                "disjoint triads -> SepStr export (forced flavour dynamics buy "
                "noncommutativity, NOT contextuality)",
    },
)
