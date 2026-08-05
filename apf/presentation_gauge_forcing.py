"""Presentation-gauge forcing: the cost trace without a cyclicity premise.

WHAT THIS MODULE ADDS, STATED AGAINST THE PRIOR ART (read this first).
The bank already carries a trace-uniqueness result: check_T_closed_loop_score_
is_normalized_trace (dense_sandwich_born.py, v24.3.434, [P_math|named_closed_
loop_leaves]) machine-closes "every normalized complex-linear CYCLIC closed-loop
score on M2(C) is Tr/2" over 8 real unknowns.  Its own key_result bills the
contribution as "the leaf-typed executable siting, not new mathematics", and it
carries CLOSED_LOOP_SCORE_CYCLICITY as a NAMED PREMISE.

This module does not rebuild that.  It REPLACES that premise.  Cyclicity is not
assumed here; it is a CONSEQUENCE.  What is assumed instead is presentation
gauge -- that the score is a function of the LOAD h = b b* rather than of the
carrier b that presents it.  The conclusion (psi = c*Tr) is the same and the
premise set is strictly weaker, and the statement generalizes off n = 2.

    prior art  :  linearity + CYCLICITY + normalization  =>  psi = Tr/2   (n=2)
    this module:  linearity + PRESENTATION GAUGE + psi(I) != 0 => psi = c*Tr (general n)
                  and cyclicity FALLS OUT (check_L_gauge_forcing_supersedes_
                  cyclicity_premise computes it).

============================================================================
STATEMENT (check_T_presentation_gauge_forces_trace, tier 4,
[P_structural | P1 open, P2 gauge, P3 underived]).

On a SINGLE block A = M_n(C), with the linear realization granted (Paper 40
rem:linear-realization; linearity is independent of the spine by
prop:linearity-independent and is INHERITED here, not removed), write the
Hermitian linear functional as psi(a) = Tr(R a) for a unique Hermitian R --
notation over C, not an assumption, and FALSE over H (see the D = H fence).

  P1  score realization: the completed route is evaluated by the sandwich
      eta_b(e) = psi(b* e b) / psi(b* b).
      STATUS: already named and already OPEN in the corpus as
      DAGGER_SANDWICH_REALIZATION / ROOTLESS_LOOP_CYCLICITY
      (operational_score_linearity.py).  NOT discharged here, NOT weakened.
  P2  loads: a preparation supplies a load h; a carrier is a factorization
      h = b b*.  The carrier is notation, the load is the object.
      STATUS: a genuine assumption about NATURE and the one an opponent denies.
      THE GAUGE ASSUMPTION LIVES HERE.  It is renamed, not removed: an opponent
      who holds the carrier itself to be physical keeps P1, P3, P4 and rejects
      the conclusion with a positive-definite non-tracial weight in hand.
      CRITERION CROSS-REF (the EDF ruling, 2026-08-04): whether a carrier
      re-presentation b -> bu is empirical-difference-free is a COMPUTED
      question, not a grantable one -- the criterion is FD1-sc profile
      preservation (the rule is encoded in the witness of
      check_FD1_structural_completeness, foundation_inputs.py; a given
      move's preservation must be computed per-site;
      Reference - DECISION - The Empirical-Difference-Free Criterion
      (2026-08-04)).  It is NOT ruled free: relative recombination-visible
      phase carries record content, so P2 stays a claim about nature and no
      grade moves.  Any future freeness argument for a fiber move shows
      profile-preservation FIRST, then invokes Clause E (delta_calculus.py).
  P3  richness: the full-support load is among the admissible preparations.
      STATUS: a genuine assumption, load-bearing, NOT derived.  At rank one the
      sandwich is invariant for EVERY weight, so the whole content of the
      requirement lives on full-support loads.
  P4  normalization: psi(I) != 0, i.e. Tr R != 0.

THEN: if eta is well defined as a function of the load -- if it depends on h and
not on the factorization chosen to write it -- then psi = c*Tr, c cancels in
eta, and eta_b(e) = Tr(rho_b e) with rho_b = b b* / Tr(b b*).

POSITIVITY IS A SEPARATE, WEAKER-CONSEQUENCE CLAUSE.  If in addition psi is
positive on positives and not identically zero (R >= 0, R != 0 -- what the cost
ledger's floor eps* > 0 supplies and Paper 40 DERIVES), then c > 0.  Positivity
buys the SIGN and nothing else: the forcing itself runs on P4.

WHY P4 AND NOT POSITIVITY -- THE PREMISE CORRECTION OF RECORD (2026-07-27).
An earlier statement of this theorem named POSITIVITY as the forcing premise and
justified it with "the trace-zero weight is excluded by positivity and by nothing
weaker".  That justification is FALSE, and check_L_presentation_gauge_invariant_
lines computes the refutation: every non-scalar invariant line, at n = 2,3,4 over
BOTH C and R, has trace zero.  So psi(I) != 0 kills every counterexample that
positivity kills -- it is strictly weaker (R = diag(2,-1) has Tr R = 1 != 0 and
is not PSD), it is what Step 2 actually divides by, and it is the natural
premise, since it says exactly that the score is DEFINED at the full-support load
P3 supplies.  Positivity is retained only for c > 0, and the bank's own
L_faithfulness_excludes_zero_not_the_sign shows the sign is not load-bearing for
the Born conclusion anyway, since c cancels.

WHICH SENSE OF "FUNCTION OF THE LOAD" -- THE SCOPE RULING OF RECORD (2026-07-27).
Two inequivalent readings were in circulation and the theorem must run on one:

  (i)  FULL-FIBRE (banked here):  invariance across the whole right-unitary
       fibre {bU : U in U(n)}.  This is what Step 1's equivalence and Step 2's
       evaluation at b = I actually use, so it is the reading the theorem is
       stated under.
  (ii) SUBGROUP:  invariance only under whichever presentations are physically
       realizable.

The difference is not cosmetic and it moves the counterexamples.  Under (i) the
trace-zero weight diag(1,-1) DOES NOT SATISFY THE HYPOTHESIS -- computed in-check
on the fixture b = [[1,2],[3,5]], U = [[3/5,-4/5],[4/5,3/5]]: same load
h = [[5,13],[13,34]], but eta_b(E00) = 3/19 while eta_bU(E00) = 9/73.  It is
excluded by the symmetry alone, with no normalization premise needed.  Under (ii)
it IS invariant, and P4 is what excludes it.  Both facts are computed below; the
theorem is banked under (i) and reading (ii) is carried as a NAMED FAILURE MODE,
which is where the sharpest falsifier lives: if only a proper subgroup of
presentations is realizable, the theorem returns a NON-TRACIAL cost functional
and a NON-BORN score.

SCOPE CORRIGENDUM OF RECORD (2026-07-27, blinded audit).  "Under (ii) P4 is what
excludes it" is TRUE ONLY FOR REALIZABLE SUBGROUPS CONTAINING THE ADMITTED
FAMILY, and that scope was not stated.  Reading (ii) as written quantifies over
an ARBITRARY realizable subgroup, and outside the admitted family there are
survivors on which P4 AND POSITIVITY BOTH HOLD and the score is still non-Born.
Two, both executed below:

    realizable subgroup = transpositions,  R = I + sigma_x/2   PSD, Tr R = 2
        b = [[1,2],[3,5]]    eta_b(E00) = 1/8     Born = 5/39
    realizable subgroup = <rotation>,      R = I + sigma_y/2   PSD, Tr R = 2
        b = [[1,i],[3,5]]    eta_b(E00) = 1/35    Born = 1/18

Each is constant across its own subgroup orbit, so each satisfies (ii); each is
positive-definite with nonzero trace, so neither P4 nor positivity touches it.
This is a SHARPER failure mode than the trace-zero one, and it is the one that
actually threatens the theorem: the trace-zero weight is a P4 story only, whereas
these survive every normalization premise the theorem has.  What excludes them is
the ADMITTED FAMILY -- they are not invariant under the quarter-phases -- so the
honest statement of the failure mode is that the theorem's protection against
(ii) is exactly the richness of the realizable presentation family, not P4.

TWO RESTRICTIONS, NEITHER COSMETIC.
  (a) DIRECT SUMS.  The conclusion is FALSE on +_i M_{n_i}.  Block-diagonal
      unitaries never mix blocks, so the constants are fixed independently and do
      not cancel.  Witness M2 + M2, R = 1*I + 3*I: every premise holds, the score
      is carrier-independent across the full block-unitary family, and the score
      is not Born (3/8 against 1/4).  Anything wanting the theorem on the full
      represented algebra owes a superselection fence or an explicit per-block-
      constant clause.  THE THEOREM IS SINGLE-BLOCK.
  (b) P4 CANNOT BE DROPPED.  At Tr R = 0 the score at b = I is 0/0 for every
      effect, Step 2 is vacuous, and a non-scalar weight survives under reading
      (ii).

WHAT IS STILL OWED (none of it closed here).
  1. P3 is not derived.  The banked symmetry_cost_floor puts the cost minimum at
     maximal symmetry, which makes the full-support load the natural candidate
     for the symmetric baseline -- a LEAD, not a result: connecting occupancy
     uniformity to h = I needs the preparation-load map, which does not exist.
  2. P1 is open and untouched.
  3. The admitted presentation family is not derived.  The forcing needs
     transpositions and quarter-phases (sufficient, not necessary -- real
     half-turns also work, which is what makes D = R go through); nothing here
     shows the corpus supplies them.
  4. Linearity is inherited, not removed.
  5. D = H is NOT COVERED.  The quaternionic trace is not cyclic, so Step 3 fails
     as written; the repair is Re Tr throughout.
  6. P2 is not derived and is the premise an opponent attacks first.

AUDIT RECORD.  Three blinded hostile cold audits.  Stage one and stage two each
found the theorem FALSE with an exact counterexample -- the direct sum, then the
trace-zero weight -- and both are carried above as restrictions rather than by
quiet narrowing.  Stage three (2026-07-27, two independent auditors, LAND-WITH-
FIXES 0.85 convergent without contact) found NO third counterexample and instead
CLOSED THE VARIETY: mu is +-1 exactly, so the sign scan is exhaustive rather
than a sample, and the enumeration below is a classification rather than a
search.  Its two MAJORs on the mathematics -- the premise correction and the
gauge-sense equivocation -- are the two rulings of record folded in above.
Report: Artifacts_2026-07-27_session/ce_born_route_audit_return/
THIRD_BLINDED_AUDIT_2026-07-27.md.

MAY NOT CITE ON THE STRENGTH OF THIS MODULE.
  - "Born is derived."  Standing corpus bar, unchanged.
  - "The trace is derived from A1."  It is derived from P1-P4, of which P1 is an
    already-open gate and P2 is a claim about nature.
  - "Presentation gauge is free" / "the argument acquires no new physical
    premise."  RETRACTED.  P2 carries it; renamed, not removed.
  - "The theorem holds on the represented algebra."  Single block only.
  - "Bare faithfulness suffices."  It does not -- but the premise is psi(I) != 0,
    NOT positivity; positivity buys only c > 0.
  - "The preparation-load theorem is closed."  It is not started.
  - "The corpus supplies the admitted presentations."  Not shown.
  - "The theorem covers D in {R, C, H}."  C proved; R proved with signed
    permutations; H NOT covered.

NON-EXPORTING.  physical_premises_certified = false.  No existing grade moved.
"""

from fractions import Fraction as F
from itertools import product
from typing import Dict, List, Sequence, Tuple

PHYSICAL_PREMISES_CERTIFIED = False
EXPORTS: Tuple[str, ...] = ()
BANK_MODIFIED = False

# --------------------------------------------------------------------------
# Exact Gaussian rationals as (re, im) pairs of Fractions.  Stdlib only.
# --------------------------------------------------------------------------

G = Tuple[F, F]
Mat = List[List[G]]

ZERO: G = (F(0), F(0))
ONE: G = (F(1), F(0))
IMAG: G = (F(0), F(1))


def _add(a: G, b: G) -> G:
    return (a[0] + b[0], a[1] + b[1])


def _sub(a: G, b: G) -> G:
    return (a[0] - b[0], a[1] - b[1])


def _mul(a: G, b: G) -> G:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def _conj(a: G) -> G:
    return (a[0], -a[1])


def _mm(A: Mat, B: Mat) -> Mat:
    n, k, m = len(A), len(B), len(B[0])
    out = []
    for i in range(n):
        row = []
        for j in range(m):
            acc = ZERO
            for t in range(k):
                acc = _add(acc, _mul(A[i][t], B[t][j]))
            row.append(acc)
        out.append(row)
    return out


def _dag(A: Mat) -> Mat:
    return [[_conj(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]


def _tr(A: Mat) -> G:
    acc = ZERO
    for i in range(len(A)):
        acc = _add(acc, A[i][i])
    return acc


def _eye(n: int) -> Mat:
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def _zeros(n: int) -> Mat:
    return [[ZERO] * n for _ in range(n)]


def _scale(c: F, A: Mat) -> Mat:
    return [[(c * x[0], c * x[1]) for x in row] for row in A]


# --------------------------------------------------------------------------
# Exact linear algebra over Q.
# --------------------------------------------------------------------------

def _rref(rows: List[List[F]]) -> Tuple[List[List[F]], List[int]]:
    M = [r[:] for r in rows]
    if not M:
        return M, []
    dim = len(M[0])
    piv: List[int] = []
    r = 0
    for c in range(dim):
        p = None
        for k in range(r, len(M)):
            if M[k][c] != 0:
                p = k
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for k in range(len(M)):
            if k != r and M[k][c] != 0:
                f = M[k][c]
                M[k] = [a - f * b for a, b in zip(M[k], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M, piv


def _nullspace(rows: List[List[F]], dim: int) -> List[List[F]]:
    if not rows:
        basis = []
        for i in range(dim):
            v = [F(0)] * dim
            v[i] = F(1)
            basis.append(v)
        return basis
    M, piv = _rref(rows)
    free = [c for c in range(dim) if c not in piv]
    out = []
    for fc in free:
        v = [F(0)] * dim
        v[fc] = F(1)
        for i, pc in enumerate(piv):
            v[pc] = -M[i][fc]
        out.append(v)
    return out


def _rank(rows: List[List[F]]) -> int:
    return len(_rref(rows)[1])


# --------------------------------------------------------------------------
# Hermitian / symmetric bases and the admitted presentation generators.
# --------------------------------------------------------------------------

def _herm_basis(n: int) -> List[Mat]:
    """Real-linear basis of the Hermitian n x n matrices; dim = n^2."""
    B: List[Mat] = []
    for i in range(n):
        M = _zeros(n)
        M[i][i] = ONE
        B.append(M)
    for i in range(n):
        for j in range(i + 1, n):
            M = _zeros(n)
            M[i][j] = ONE
            M[j][i] = ONE
            B.append(M)
            M = _zeros(n)
            M[i][j] = IMAG
            M[j][i] = (F(0), F(-1))
            B.append(M)
    return B


def _sym_basis(n: int) -> List[Mat]:
    """Real-linear basis of the real symmetric n x n matrices; dim = n(n+1)/2."""
    B: List[Mat] = []
    for i in range(n):
        M = _zeros(n)
        M[i][i] = ONE
        B.append(M)
    for i in range(n):
        for j in range(i + 1, n):
            M = _zeros(n)
            M[i][j] = ONE
            M[j][i] = ONE
            B.append(M)
    return B


def _transpositions(n: int) -> List[Mat]:
    out = []
    for i in range(n - 1):
        M = _eye(n)
        M[i][i] = ZERO
        M[i + 1][i + 1] = ZERO
        M[i][i + 1] = ONE
        M[i + 1][i] = ONE
        out.append(M)
    return out


def _quarter_phases(n: int) -> List[Mat]:
    out = []
    for i in range(n):
        M = _eye(n)
        M[i][i] = IMAG
        out.append(M)
    return out


def _sign_flips(n: int) -> List[Mat]:
    out = []
    for i in range(n):
        M = _eye(n)
        M[i][i] = (F(-1), F(0))
        out.append(M)
    return out


def _complex_generators(n: int) -> List[Mat]:
    return _transpositions(n) + _quarter_phases(n)


def _real_generators(n: int) -> List[Mat]:
    return _transpositions(n) + _sign_flips(n)


# --------------------------------------------------------------------------
# The graded invariance system:  g R g* = s_g * R  for each generator g.
# --------------------------------------------------------------------------

def _graded_solutions(basis: List[Mat], gens: Sequence[Mat],
                      signs: Sequence[int], n: int) -> List[Mat]:
    """Every R in span(basis) with g R g* = s_g R for all generators."""
    dim = len(basis)
    cols: List[List[F]] = []
    for k in range(dim):
        col: List[F] = []
        for g, s in zip(gens, signs):
            Mk = _mm(_mm(g, basis[k]), _dag(g))
            for a in range(n):
                for b in range(n):
                    col.append(Mk[a][b][0] - s * basis[k][a][b][0])
                    col.append(Mk[a][b][1] - s * basis[k][a][b][1])
        cols.append(col)
    rows = [[cols[k][r] for k in range(dim)] for r in range(len(cols[0]))]
    out = []
    for v in _nullspace(rows, dim):
        R = _zeros(n)
        for k, coef in enumerate(v):
            for a in range(n):
                for b in range(n):
                    R[a][b] = _add(R[a][b],
                                   (coef * basis[k][a][b][0],
                                    coef * basis[k][a][b][1]))
        out.append(R)
    return out


def _is_scalar(R: Mat, n: int) -> bool:
    off = all(R[a][b] == ZERO for a in range(n) for b in range(n) if a != b)
    return off and len({R[i][i] for i in range(n)}) == 1


def _is_psd(R: Mat, n: int) -> bool:
    """Exact PSD test: every principal minor of every principal submatrix >= 0."""
    from itertools import combinations

    def det(sub: Mat) -> G:
        m = len(sub)
        if m == 0:
            return ONE
        if m == 1:
            return sub[0][0]
        acc = ZERO
        for j in range(m):
            minor = [[sub[i][k] for k in range(m) if k != j] for i in range(1, m)]
            term = _mul(sub[0][j], det(minor))
            acc = _add(acc, term if j % 2 == 0 else (-term[0], -term[1]))
        return acc

    for size in range(1, n + 1):
        for idx in combinations(range(n), size):
            sub = [[R[i][j] for j in idx] for i in idx]
            d = det(sub)
            if d[1] != 0 or d[0] < 0:
                return False
    return True


# --------------------------------------------------------------------------
# The sandwich score.
# --------------------------------------------------------------------------

def _score(R: Mat, b: Mat, e: Mat):
    """eta_b(e) = Tr(R b* e b) / Tr(R b* b); None when the denominator vanishes."""
    num = _tr(_mm(R, _mm(_dag(b), _mm(e, b))))
    den = _tr(_mm(R, _mm(_dag(b), b)))
    if den == ZERO:
        return None
    if num[1] != 0 or den[1] != 0:
        return None
    return num[0] / den[0]


def _born(h: Mat, e: Mat):
    num = _tr(_mm(h, e))
    den = _tr(h)
    if den == ZERO:
        return None
    return num[0] / den[0]


def _effects(n: int) -> List[Mat]:
    """A spanning family inside 0 <= e <= I: diagonal units and real/imag halves."""
    out = []
    for i in range(n):
        M = _zeros(n)
        M[i][i] = ONE
        out.append(M)
    half = F(1, 2)
    for i in range(n):
        for j in range(i + 1, n):
            M = _zeros(n)
            M[i][i] = (half, F(0))
            M[j][j] = (half, F(0))
            M[i][j] = (half, F(0))
            M[j][i] = (half, F(0))
            out.append(M)
            M = _zeros(n)
            M[i][i] = (half, F(0))
            M[j][j] = (half, F(0))
            M[i][j] = (F(0), half)
            M[j][i] = (F(0), -half)
            out.append(M)
    return out


def _result(name, epistemic, key_result, evidence, fails, tier,
            dependencies, premises, negative_controls, cross_refs):
    return {
        'name': name,
        'epistemic': epistemic,
        'passed': not fails,
        'tier': tier,
        'key_result': key_result,
        'evidence': evidence,
        'fail_reasons': fails,
        'dependencies': list(dependencies),
        'premises': list(premises),
        'negative_controls': list(negative_controls),
        'cross_refs': list(cross_refs),
        'physical_premises_certified': PHYSICAL_PREMISES_CERTIFIED,
        'exports': list(EXPORTS),
        'bank_modified': BANK_MODIFIED,
    }


# ==========================================================================
# LEG 1 -- the closed classification of invariant lines.
# ==========================================================================

def check_L_presentation_gauge_invariant_lines() -> Dict[str, object]:
    """Tier 3, [P_math].  Every invariant line, enumerated; non-scalar => Tr = 0."""
    fails: List[str] = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)

    # ---- Step A: mu is +-1 EXACTLY, so the sign scan is exhaustive. --------
    # U R U* is Hermitian with the spectrum of R, so Tr((URU*)^2) = Tr(R^2).
    # If U R U* = mu R with R != 0 Hermitian then mu^2 Tr(R^2) = Tr(R^2) and
    # Tr(R^2) > 0, hence mu^2 = 1.  Executed rather than asserted: verify the
    # conjugation is Tr(R^2)-preserving on a battery, and that Tr(R^2) > 0 for
    # every nonzero Hermitian witness.
    frob_preserved = 0
    positive_frob = 0
    for n in (2, 3):
        for Rb in _herm_basis(n):
            t2 = _tr(_mm(Rb, Rb))
            ck(t2[1] == 0 and t2[0] > 0,
               f"Tr(R^2) must be real and > 0 for a nonzero Hermitian R (n={n})")
            positive_frob += 1
            for g in _complex_generators(n):
                conj = _mm(_mm(g, Rb), _dag(g))
                if _tr(_mm(conj, conj)) == t2:
                    frob_preserved += 1
                else:
                    fails.append(f"conjugation failed to preserve Tr(R^2) (n={n})")
    ck(frob_preserved > 0, "the Frobenius-preservation battery must be non-empty")

    # ---- Step B: enumerate every invariant line, both fields. --------------
    # CORRIGENDUM OF RECORD (2026-07-27, blinded audit).  _graded_solutions
    # returns a BASIS of each graded solution space, not its lines.  When a
    # graded space has dimension >= 2 the invariant LINES form a projective
    # space and any predicate applied to the returned spanning vectors tests
    # only those vectors -- so "every non-scalar invariant line has trace zero"
    # would be a statement about an RREF artefact rather than about the variety.
    # It is TRUE for the admitted family because every graded space here is
    # ONE-dimensional, and that is now ASSERTED rather than relied on: with
    # dim <= 1 a spanning vector IS the line, and Step C's predicates are
    # statements about the variety.  Counterexample showing the assertion is
    # load-bearing and not decorative: under transpositions ALONE the +1 space
    # is 2-dimensional and contains R = I + sigma_x/2, which is non-scalar, PSD,
    # and has trace 2 -- so on a wider generator set the Step C predicates would
    # pass while their claim is false.  That control is executed in Step D.
    lines: Dict[str, List[Dict[str, object]]] = {}
    space_dims: Dict[str, List[int]] = {}
    for field, basis_fn, gen_fn in (("C", _herm_basis, _complex_generators),
                                    ("R", _sym_basis, _real_generators)):
        for n in (2, 3, 4):
            gens = gen_fn(n)
            basis = basis_fn(n)
            seen = []
            recs: List[Dict[str, object]] = []
            dims: List[int] = []
            for signs in product((1, -1), repeat=len(gens)):
                _sols_here = _graded_solutions(basis, gens, signs, n)
                dims.append(len(_sols_here))
                ck(len(_sols_here) <= 1,
                   f"Step B: every graded solution space must be at most "
                   f"ONE-dimensional ({field}{n}, signs={signs}, got "
                   f"{len(_sols_here)}) -- otherwise the returned vectors are an "
                   f"RREF basis and Step C tests an artefact, not the lines")
                for R in _sols_here:
                    key = tuple(tuple(x) for row in R for x in row)
                    if key in seen:
                        continue
                    seen.append(key)
                    tr = _tr(R)
                    recs.append({
                        "scalar": _is_scalar(R, n),
                        "trace_re": str(tr[0]),
                        "psd": _is_psd(R, n),
                    })
            # (loop body unchanged; the enclosing scan now pins the dimension)
            lines[f"{field}{n}"] = recs
            space_dims[f"{field}{n}"] = dims

    # ---- Step C: the classification claim, computed. ----------------------
    non_scalar_total = 0
    for tag, recs in lines.items():
        ck(any(r["scalar"] for r in recs),
           f"the scalar line must always survive ({tag})")
        psd_lines = [r for r in recs if r["psd"]]
        ck(len(psd_lines) == 1 and psd_lines[0]["scalar"] is True,
           f"exactly one invariant line may be PSD, and it must be the scalar one ({tag})")
        for r in recs:
            if not r["scalar"]:
                non_scalar_total += 1
                ck(r["trace_re"] == "0",
                   f"a non-scalar invariant line must have trace zero ({tag}, "
                   f"trace={r['trace_re']}) -- this is the claim that makes "
                   f"psi(I) != 0 sufficient and positivity unnecessary")
    ck(non_scalar_total > 0,
       "ANTI-VACUITY: the enumeration must actually FIND non-scalar lines, "
       "or the trace-zero claim is empty")

    # ---- Step D: negative control -- a proper subgroup leaves more. --------
    # Permutations alone must NOT force scalarity, at every n tested.  If this
    # passed, the forcing would be attributed to the wrong generators.
    subgroup_survivors = {}
    for n in (2, 3, 4):
        basis = _herm_basis(n)
        perms = _transpositions(n)
        sols = _graded_solutions(basis, perms, [1] * len(perms), n)
        subgroup_survivors[f"C{n}"] = len(sols)
        ck(len(sols) > 1,
           f"NEGATIVE CONTROL: permutations alone must leave more than the "
           f"scalar line (n={n}) -- they do not force the trace")

    # ---- Step D1: the OTHER half of that control -- quarter-phases alone. --
    # THIS LEG ANSWERS TO THE PROPOSITION'S PROOF, NOT TO ITS STATEMENT.  The
    # statement of prop:presentation-gauge-trace quantifies over EVERY unitary;
    # its proof needs exactly two families and says, in prose, what each of them
    # alone leaves -- "Each generator alone therefore imposes rank two on
    # (a,d,x,y) and leaves a two-parameter family --- an unequal diagonal
    # survives the phase, and an equal-diagonal real off-diagonal survives the
    # swap" -- and at general n, "the permutations equalize the diagonal entries
    # of R, and independent quarter-phases on distinct coordinates force
    # i^{k_j-k_k} R_{jk} = R_{jk} for all admissible choices, hence R_{jk} = 0
    # off the diagonal".  The SWAP half of that sentence is Step D above.  The
    # PHASE half was asserted in prose and never executed, with the generator
    # helper for it already in this file.  It is executed here, and the two
    # halves together make Step D a DECOMPOSITION of the forcing rather than a
    # one-sided sanity check: each half alone leaves strictly more than the
    # scalar line, for a DIFFERENT reason, and their intersection is the scalar
    # line the theorem runs on.
    #
    # WHAT MAY BE READ OFF THE RETURNED BASIS AND WHAT MAY NOT.
    # _graded_solutions returns an RREF BASIS of the solution space, not its
    # lines -- the corrigendum of record in Step B.  A predicate applied to that
    # basis is a statement about the SPAN only if its truth set is closed under
    # linear combination.  DIAGONALITY IS SUCH A PREDICATE, since the diagonal
    # matrices are a subspace; PSD AND TRACE-NONZERO ARE NOT, which is exactly
    # the error class the corrigendum caught.  That difference is not asserted
    # here, it is EXHIBITED: this very space contains diag(1,-1,0,...,0), which
    # is invariant, diagonal, non-scalar and NOT PSD, so a PSD reading of this
    # basis would be true of the basis and false of the space, while the
    # diagonal reading transfers.  Because the phase half alone does not equalize
    # the diagonal, a non-scalar trace-zero survivor here is expected and is no
    # counterexample to Step C, which quantifies over the ADMITTED family.
    #
    # And the claim is made SET-EXACT rather than dimensional, in both
    # directions, with the dimension read off the computation:
    #     span(returned) <= diagonals  -- every returned vector is diagonal;
    #     diagonals <= solution space  -- every E_ii is verified invariant;
    #     dim = n                      -- computed, then compared to n.
    # The solver is verified rather than trusted: every returned vector is
    # checked to satisfy g R g* = R directly, so a count-correct basis of the
    # wrong space is caught instead of absorbed.
    phase_survivors: Dict[str, int] = {}
    perm_survivors: Dict[str, int] = {}
    both_survivors: Dict[str, int] = {}
    phase_space_exactly_diagonal: Dict[str, bool] = {}
    phase_blocks_certified: Dict[str, bool] = {}
    for n in (2, 3, 4):
        basis = _herm_basis(n)
        phases = _quarter_phases(n)
        gens_all = _complex_generators(n)
        tag = f"C{n}"

        # (a) The two controls must PARTITION the admitted family, or they are
        #     two isolated facts about two unrelated groups rather than a
        #     decomposition of this theorem's forcing.
        ck(_transpositions(n) + phases == gens_all,
           f"Step D1: the two controls must partition the admitted family "
           f"({tag}) -- transpositions + quarter-phases must BE the admitted "
           f"generator list, or the decomposition claim is empty")

        # (b) And the phase half must really be QUARTER-phases: one per
        #     coordinate, diagonal, unitary, of order EXACTLY four.  Sign flips
        #     are diagonal, unitary, one per coordinate, and leave the SAME
        #     diagonal space -- for the wrong reason and over the wrong field --
        #     so nothing downstream distinguishes them and this leg must.
        #     WELL-FORMEDNESS GATE, AND ITS HONEST SCOPE.  Every leg below
        #     conjugates by a generator or indexes the family by coordinate, so
        #     the gate is what keeps THIS leg from raising on a malformed
        #     family.  It does NOT make the CHECK crash-proof, and the earlier
        #     comment here said it did.  A shape-malformed family is consumed by
        #     Step A, ~85 lines upstream, which performs the same conjugation on
        #     the same generators and raises there first; that is PRE-EXISTING
        #     -- the banked file raises identically -- and it is outside this
        #     extension's remit to repair.  Second audit, mutation M5.
        shape_ok = all(isinstance(g, list) and len(g) == n
                       and all(isinstance(row, list) and len(row) == n
                               for row in g)
                       for g in phases)
        ck(shape_ok,
           f"Step D1: every phase generator must be an n x n matrix ({tag})")
        ck(len(phases) == n,
           f"Step D1: there must be one quarter-phase per coordinate ({tag}, "
           f"got {len(phases)})")
        family_ok = bool(shape_ok and len(phases) == n)
        if not family_ok:
            #     A malformed family is dropped HERE, after the two assertions
            #     above have already recorded the failure, so that D1's own
            #     legs are not handed a matrix they cannot index.
            #     CAVEAT, and it is why the dimension leg's message must be read
            #     with the family legs above it: the empty family leaves the
            #     WHOLE AMBIENT invariant, so the dimension leg below reports
            #     n^2 and its message quotes that number -- which is a fact
            #     about the substitution, NOT about the malformed family's own
            #     invariant space.  The family legs above carry the real cause.
            #     Second audit, mutation M2.
            phases = []
        diag_sigs = set()
        for g in (phases if family_ok else ()):
            g2 = _mm(g, g)
            ck(_mm(g, _dag(g)) == _eye(n),
               f"Step D1: each phase generator must be unitary ({tag})")
            ck(all(g[a][b] == ZERO for a in range(n) for b in range(n)
                   if a != b),
               f"Step D1: each phase generator must be diagonal ({tag})")
            ck(_mm(g2, g2) == _eye(n) and g2 != _eye(n),
               f"Step D1: each phase generator must have order EXACTLY four "
               f"({tag}) -- order two would be a SIGN FLIP, which leaves the "
               f"same diagonal space and would make this control a statement "
               f"about the wrong family")
            diag_sigs.add(tuple(g[i][i] for i in range(n)))
        ck(family_ok and len(diag_sigs) == n,
           f"Step D1: the phases must sit on DISTINCT coordinates ({tag}, "
           f"{len(diag_sigs)} distinct of {n}; family well-formed: "
           f"{family_ok}) -- the proof's clause is 'independent quarter-phases "
           f"on distinct coordinates', and a malformed family reports zero "
           f"distinct coordinates here rather than raising")

        #      AND THE PREDICATE ITSELF, not a proxy for it.  Distinct diagonal
        #      signatures is a COUNT; "one quarter-phase per coordinate" is a
        #      STATEMENT ABOUT SUPPORT, and a family can satisfy the count while
        #      failing the statement.  Two families do exactly that: phases[i]
        #      carrying i at coordinate i and -i at coordinate i+1 mod n, and
        #      the family D_0..D_{n-2} together with i*I.  Both are diagonal,
        #      unitary, of order four, n in number and pairwise distinct; both
        #      generate a PROPER SUBGROUP of (Z/4)^n, so neither is "all
        #      admissible choices of i^{k_j}"; and neither is supported on one
        #      coordinate.  The proxy admits both.  The predicate does not.
        #      This assertion also supplies the index convention that leg (c1)
        #      below reads -- it takes phases[j] for the block at (j,k) -- which
        #      was otherwise true only by construction and unstated, so a
        #      REORDERING of the helper made (c1) fail with a message blaming
        #      the mathematics.  Found by a foreign audit, three escapes, one
        #      assertion.
        #      EITHER quarter-phase at coordinate i is admissible: i and -i
        #      generate the same Z/4 and the proof quantifies over ALL
        #      admissible choices of i^{k_j}, so pinning to +i alone would
        #      reject an equivalent family -- a false rejection, found by the
        #      second audit.  What must be pinned is the SUPPORT.
        quarter_at_i = (IMAG, (F(0), F(-1)))
        ck(all(phases[i][i][i] in quarter_at_i
               and all(phases[i][a][a] == ONE for a in range(n) if a != i)
               for i in (range(n) if family_ok else ())) and family_ok,
           f"Step D1: phases[i] must be A quarter-phase supported on "
           f"coordinate i and the identity elsewhere ({tag}) -- 'independent "
           f"quarter-phases on distinct coordinates' is a statement about "
           f"SUPPORT, not about which of the two quarter-phases is used, and "
           f"leg (c1) reads phases[j] for the block at (j,k)")

        # (b2) THE OTHER HALF OF THE DECOMPOSITION, pinned to the same
        #      standard.  Step D asserts only that permutations alone leave
        #      MORE than the scalar line -- a bare inequality -- while the
        #      key_result now describes the pair as a decomposition and quotes a
        #      dimension.  An inequality does not carry a number.  A foreign
        #      audit deleted one constraint row from the solver, moved
        #      permutations-alone from 2 to 3/5/8 at n = 2/3/4, and the check
        #      stayed green with the prose one field away still reading
        #      "dimension 2".  Pinned here, in D1, so Step D is untouched and
        #      this remains an extension.
        perm_sols = _graded_solutions(basis, _transpositions(n),
                                      [1] * len(_transpositions(n)), n)
        perm_survivors[tag] = len(perm_sols)
        ck(len(perm_sols) == 2,
           f"Step D1: permutations alone must leave EXACTLY a two-dimensional "
           f"space ({tag}: computed {len(perm_sols)}) -- Step D's inequality "
           f"does not carry the number the key_result quotes")
        #      And the proof's own clause for this half -- "the permutations
        #      equalize the diagonal entries of R" -- executed rather than
        #      quoted: every returned vector has a constant diagonal.
        ck(all(len({R[i][i] for i in range(n)}) == 1 for R in perm_sols),
           f"Step D1: permutations alone must EQUALIZE THE DIAGONAL ({tag}) "
           f"-- that is the proof's clause for this half, and Step D never "
           f"executes it")

        # (c0) THE AMBIENT, pinned SET-EXACTLY.  "Exactly the diagonal" is a
        #      claim about a space, and it is the intended claim only if the
        #      ambient is the FULL n^2-dimensional Hermitian space.  Shrink the
        #      ambient -- drop the imaginary off-diagonal directions, say -- and
        #      every assertion below still passes while meaning something
        #      strictly weaker.  So the ambient is pinned against the standard
        #      basis by membership, not by count alone.
        diag_units = []
        for i in range(n):
            E = _zeros(n)
            E[i][i] = ONE
            diag_units.append(E)
        blocks = []
        for j in range(n):
            for k in range(j + 1, n):
                X = _zeros(n)
                X[j][k] = ONE
                X[k][j] = ONE
                Y = _zeros(n)
                Y[j][k] = IMAG
                Y[k][j] = (F(0), F(-1))
                blocks.append((j, k, X, Y))
        expected_basis = diag_units + [M for (_, _, X, Y) in blocks
                                       for M in (X, Y)]
        missing = sum(1 for M in expected_basis if M not in basis)
        ck(len(basis) == n * n and len(expected_basis) == n * n
           and missing == 0,
           f"Step D1: the ambient must be the FULL n^2-dimensional Hermitian "
           f"space ({tag}: |basis| = {len(basis)}, n^2 = {n * n}, {missing} "
           f"standard directions missing) -- on a smaller ambient 'exactly the "
           f"diagonal' is a weaker claim wearing the same words")

        # (c1) THE UPPER CONTAINMENT, CERTIFIED WITHOUT THE SOLVER.
        #      The one thing an RREF basis cannot certify about itself is that
        #      it SPANS: a solver that under-returns yields a solution space
        #      strictly larger than the diagonals while every returned vector is
        #      still diagonal.  So the upper bound is established independently.
        #      Each quarter-phase is diagonal, hence conjugation preserves the
        #      decomposition of the Hermitian space into the n diagonal units
        #      and the n(n-1)/2 two-dimensional off-diagonal blocks; on the
        #      block at (j,k) the generator acts by the 2x2 real matrix M read
        #      off the (j,k) entry, and the block contributes a nonzero
        #      invariant iff M - I is singular.  Both facts are computed: that
        #      the block is preserved, and that det(M - I) != 0.  This is the
        #      executable form of the proof's "independent quarter-phases on
        #      distinct coordinates force i^{k_j-k_k} R_{jk} = R_{jk}, hence
        #      R_{jk} = 0 off the diagonal".
        blocks_closed = 0
        blocks_rigid = 0
        for (j, k, X, Y) in (blocks if family_ok else ()):
            g = phases[j]
            coefs = []
            closed = True
            for B in (X, Y):
                C = _mm(_mm(g, B), _dag(g))
                if any(C[a][b] != ZERO for a in range(n) for b in range(n)
                       if (a, b) != (j, k) and (a, b) != (k, j)):
                    closed = False
                coefs.append((C[j][k][0], C[j][k][1]))
            if not closed:
                continue
            blocks_closed += 1
            (a11, a21), (a12, a22) = coefs
            if (a11 - 1) * (a22 - 1) - a12 * a21 != 0:
                blocks_rigid += 1
        ck(family_ok and blocks_closed == len(blocks),
           f"Step D1: conjugation by a quarter-phase must preserve every "
           f"off-diagonal block ({tag}: {blocks_closed} of {len(blocks)}; "
           f"family well-formed: {family_ok}) -- the block argument is valid "
           f"only for DIAGONAL generators")
        ck(family_ok and blocks_rigid == len(blocks),
           f"Step D1: M - I must be nonsingular on every off-diagonal block "
           f"({tag}: {blocks_rigid} of {len(blocks)}) -- this is the upper "
           f"containment solution space <= diagonals, and it is the half no "
           f"returned basis can certify about itself, since a solver that "
           f"under-returns leaves every returned vector diagonal")
        phase_blocks_certified[tag] = bool(family_ok
                                           and blocks_closed == len(blocks)
                                           and blocks_rigid == len(blocks)
                                           and len(blocks) == n * (n - 1) // 2)


        # (c) The surviving space, computed.
        sols = _graded_solutions(basis, phases, [1] * len(phases), n)
        dim = len(sols)
        phase_survivors[tag] = dim

        sols_shape_ok = all(len(R) == n and all(len(row) == n for row in R)
                            for R in sols)
        ck(sols_shape_ok,
           f"Step D1: every returned vector must be an n x n matrix ({tag})")
        probe_ok = bool(family_ok and sols_shape_ok)
        not_invariant = (sum(1 for R in sols
                             if any(_mm(_mm(g, R), _dag(g)) != R
                                    for g in phases))
                         if probe_ok else -1)
        ck(not_invariant == 0,
           f"Step D1: every returned vector must actually satisfy g R g* = R "
           f"({tag}, {not_invariant} of {dim} do not; -1 means the family or "
           f"the returned shapes were malformed and this leg DID NOT RUN, "
           f"which is not the same as passing) -- the solver is verified, not "
           f"trusted")

        ck(dim > 1,
           f"NEGATIVE CONTROL: quarter-phases alone must leave more than the "
           f"scalar line ({tag}, computed dimension {dim}) -- they do not force "
           f"the trace either, and the complementary control is Step D")

        ck(dim == n,
           f"Step D1: quarter-phases alone must leave exactly the "
           f"n-dimensional diagonal ({tag}: computed {dim}, claimed {n})")

        off_diag_offenders = (sum(1 for R in sols
                                  if any(R[a][b] != ZERO
                                         for a in range(n) for b in range(n)
                                         if a != b))
                              if sols_shape_ok else -1)
        ck(off_diag_offenders == 0,
           f"Step D1: every returned vector must be DIAGONAL ({tag}, "
           f"{off_diag_offenders} of {dim} carry an off-diagonal entry) -- this "
           f"is the content of the phase half, and diagonality is a SUBSPACE "
           f"predicate, so basis-wise truth is a statement about the span")

        diag_units_invariant = 0
        for i in (range(n) if family_ok else ()):
            E = _zeros(n)
            E[i][i] = ONE
            if all(_mm(_mm(g, E), _dag(g)) == E for g in phases):
                diag_units_invariant += 1
        ck(diag_units_invariant == n,
           f"Step D1: every diagonal matrix unit must be phase-invariant "
           f"({tag}: {diag_units_invariant} of {n}) -- this is the containment "
           f"diagonals <= solution space, which no dimension count supplies")

        #      AND THE OTHER HALF OF THE CONTRAST, computed.  The comment
        #      block above says a PSD reading of this basis "would be true of
        #      the basis and false of the space".  The false-of-the-space half
        #      is pinned by the W witness.  The true-of-the-basis half was
        #      asserted and never tested; it is one line, so it is tested.
        #      Second audit, MINOR-2.
        ck(all(_is_psd(R, n) for R in sols) and all(_tr(R)[0] != ZERO[0]
                                                    for R in sols),
           f"Step D1: every returned basis vector must be PSD with nonzero "
           f"trace ({tag}) -- that is the 'true of the basis' half of the "
           f"contrast this block claims, and without it the contrast is prose")

        phase_space_exactly_diagonal[tag] = bool(
            probe_ok and dim == n and off_diag_offenders == 0
            and diag_units_invariant == n and not_invariant == 0)

        # The predicate-transfer witness, exhibited on this space.
        W = _zeros(n)
        W[0][0] = ONE
        W[1][1] = (F(-1), F(0))
        ck(family_ok and all(_mm(_mm(g, W), _dag(g)) == W for g in phases),
           f"Step D1: diag(1,-1,0,...) must be phase-invariant ({tag}; family "
           f"well-formed: {family_ok}) -- the witness that this space is bigger "
           f"than a line")
        ck(not _is_psd(W, n) and not _is_scalar(W, n) and _tr(W)[0] == 0,
           f"Step D1: and it must be NON-PSD, non-scalar and trace-zero ({tag}) "
           f"-- so a PSD or trace reading of the returned RREF basis would be an "
           f"artefact here, while the diagonal reading transfers to every line")

        # (d) THE PAIR.  Each half alone leaves strictly more; together they
        #     leave dimension one, and it is the scalar line.
        both = _graded_solutions(basis, gens_all, [1] * len(gens_all), n)
        both_survivors[tag] = len(both)
        ck(len(both) == 1,
           f"Step D1: the two halves TOGETHER must leave dimension ONE ({tag}, "
           f"computed {len(both)}) -- otherwise the two controls do not "
           f"decompose the forcing, they merely coexist")
        ck(len(both) == 1 and _is_scalar(both[0], n),
           f"Step D1: and the single surviving line must be the SCALAR line "
           f"({tag})")

    # (e) COVERAGE CONTRACT.  An empty `fails` is returned both by a leg whose
    #     assertions passed and by a leg that never ran, so the sweep is counted
    #     by name rather than left to the loop.
    ck(sorted(phase_survivors) == ["C2", "C3", "C4"],
       f"Step D1 ANTI-VACUITY: the phases-alone control must have run at "
       f"n = 2,3,4 (ran: {sorted(phase_survivors)})")
    ck(sorted(both_survivors) == ["C2", "C3", "C4"],
       f"Step D1 ANTI-VACUITY: the both-halves pairing must have run at "
       f"n = 2,3,4 (ran: {sorted(both_survivors)})")
    #      Step D and Step D1 each solve for permutations-alone, independently.
    #      Two calls for one quantity that nothing compares is two numbers that
    #      can drift apart in silence -- and the second audit found that the new
    #      key had been silently OVERWRITING Step D's banked field, so the
    #      divergence would not even have been visible in the evidence.
    ck(subgroup_survivors == perm_survivors,
       f"Step D1 coverage: Step D and Step D1 must agree on permutations-alone "
       f"(Step D {subgroup_survivors} vs Step D1 {perm_survivors}) -- they are "
       f"two independent solves of one quantity and nothing else ties them")
    ck(all(perm_survivors.get(t) == 2 for t in ("C2", "C3", "C4")),
       f"Step D1 coverage: permutations-alone must be pinned at every n "
       f"(recorded: {sorted(perm_survivors)})")
    ck(all(phase_blocks_certified.get(t) is True
           for t in ("C2", "C3", "C4")),
       f"Step D1 ANTI-VACUITY: the solver-independent upper containment must "
       f"be certified at every n (recorded: {sorted(phase_blocks_certified)})")
    ck(all(phase_space_exactly_diagonal.get(t) is True
           for t in ("C2", "C3", "C4")),
       f"Step D1 ANTI-VACUITY: the exactly-diagonal verdict must be recorded "
       f"and TRUE at every n (recorded: {sorted(phase_space_exactly_diagonal)})")

    # ---- Step D2: WHY the dimension pin in Step B is load-bearing. ---------
    # On a wider graded space the Step C predicates would report "pass" while
    # their claim is FALSE.  Exhibited, not asserted: under transpositions alone
    # at n = 2 the +1 space is 2-dimensional, and I + sigma_x/2 lies in it --
    # invariant, NON-scalar, PSD, and trace 2.  Any predicate keyed to returned
    # spanning vectors can miss it; the dimension pin is what makes Step C a
    # statement about the variety rather than about an RREF artefact.
    Rx = [[ONE, (F(1, 2), F(0))], [(F(1, 2), F(0)), ONE]]
    perm2 = _transpositions(2)
    ck(all(_mm(_mm(g, Rx), _dag(g)) == Rx for g in perm2),
       "Step D2: the wider-space witness must be invariant under the "
       "permutation subgroup")
    ck(not _is_scalar(Rx, 2) and _is_psd(Rx, 2) and _tr(Rx)[0] == 2,
       "Step D2: and it must be NON-scalar, PSD, and trace-NONZERO -- the exact "
       "shape Step C's predicates forbid, surviving on a wider graded space")
    ck(len(_graded_solutions(_herm_basis(2), perm2, [1] * len(perm2), 2)) > 1,
       "Step D2: and the space it lives in must actually be >1-dimensional, or "
       "the witness proves nothing about the dimension pin")

    key = (
        "THE VARIETY IS CLOSED, not sampled. Well-definedness of a RATIO imposes "
        "only U R U* = mu(U) R; mu = +-1 EXACTLY (U R U* is Hermitian with the "
        "spectrum of R, so Tr((URU*)^2) = Tr(R^2), and Tr(R^2) > 0 for R != 0), "
        "so scanning sign vectors over the generators is EXHAUSTIVE over all "
        "invariant lines rather than a search. Enumerated at n = 2,3,4 over BOTH "
        "C (transpositions + quarter-phases, Hermitian) and R (transpositions + "
        "sign flips, symmetric): EVERY non-scalar invariant line has TRACE ZERO, "
        "and in every case exactly one line is PSD -- the scalar one. CONSEQUENCE, "
        "and the reason this leg exists: psi(I) != 0 excludes every non-scalar "
        "survivor, so it is SUFFICIENT for the forcing and POSITIVITY IS NOT "
        "NEEDED for it (positivity buys only c > 0). Over R at n = 2 the "
        "non-scalar survivors are TWO -- diag(1,-1) and [[0,1],[1,0]] -- so the "
        "loophole is two-dimensional there, not one. NEGATIVE CONTROL, BOTH "
        "HALVES -- this is a decomposition of the forcing, not a one-sided "
        "sanity check, and it answers to the proposition's PROOF, which needs "
        "only two generator families, rather than to its statement, which "
        "quantifies over every unitary. Permutations alone leave strictly more "
        "than the scalar line at every n (dimension 2 at n = 2,3,4), so the "
        "forcing is not attributable to relabelling. Quarter-phases alone leave "
        "strictly more too, and WHAT they leave is computed and pinned "
        "set-exactly: EXACTLY the diagonal subspace, dimension 2, 3, 4 at "
        "n = 2, 3, 4 -- every returned vector diagonal (span <= diagonals, a "
        "SUBSPACE predicate, so basis-wise truth transfers to every line) and "
        "every diagonal matrix unit invariant (diagonals <= solution space), "
        "with every returned vector verified to satisfy g R g* = R rather than "
        "trusted from the solver. The upper containment does not rest on the "
        "solver at all: since the quarter-phases are diagonal they preserve the "
        "splitting of the Hermitian space into n diagonal units and n(n-1)/2 "
        "two-dimensional off-diagonal blocks, and on every block M - I is "
        "nonsingular, which is the executable form of the proof's clause and is "
        "the half a returned RREF basis cannot certify about itself, a solver "
        "that under-returns leaving every returned vector diagonal. The ambient "
        "is pinned set-exactly to the full n^2-dimensional Hermitian space, "
        "since on a smaller ambient the same words carry a weaker claim. The two halves TOGETHER leave dimension one "
        "and it is the scalar line, so each family alone is insufficient and "
        "the intersection is what forces the trace. The contrast that makes the "
        "predicate choice load-bearing is exhibited on this same space: "
        "diag(1,-1,0,...) is invariant, non-scalar, trace-zero and NOT PSD, so "
        "a PSD or trace reading of an RREF basis would be an artefact while the "
        "diagonal reading is exact. SCOPE OF 'CLOSED' "
        "(corrigendum of record, 2026-07-27, blinded audit): the enumeration "
        "returns a BASIS of each graded space, so the trace-zero and PSD "
        "predicates are statements about invariant LINES only because every "
        "graded space here is ONE-dimensional -- now asserted in Step B rather "
        "than relied on. Step D2 exhibits what the pin buys: under transpositions "
        "alone the +1 space is 2-dimensional and contains I + sigma_x/2, which is "
        "non-scalar, PSD and trace 2, so on a wider generator set the predicates "
        "would report pass while their claim is false. The closure claim is "
        "therefore scoped to the admitted family, where it is exact."
    )
    return _result(
        'L_presentation_gauge_invariant_lines',
        'P_math -- exact finite enumeration over Q; no physical premise consumed',
        key,
        {
            "invariant_lines_by_field_and_n": lines,
            "non_scalar_lines_found": non_scalar_total,
            "frobenius_preservation_checks": frob_preserved,
            "nonzero_hermitian_positive_frobenius": positive_frob,
            "subgroup_control_permutations_only_survivors": subgroup_survivors,
            "subgroup_control_phases_only_survivors": phase_survivors,
            "subgroup_control_permutations_only_survivors_pinned":
                perm_survivors,
            "phases_only_space_is_exactly_diagonal": phase_space_exactly_diagonal,
            "phases_only_upper_containment_certified_without_solver":
                phase_blocks_certified,
            "admitted_family_both_halves_survivors": both_survivors,
            "graded_space_dimensions": space_dims,
            "wider_space_witness": "I + sigma_x/2 under transpositions alone: "
                                   "non-scalar, PSD, trace 2",
            "mu_restricted_to": "{+1, -1}",
        },
        fails,
        3,
        (),
        (),
        ("permutations alone must not force scalarity",
         "quarter-phases alone must not force scalarity either: they leave "
         "EXACTLY the n-dimensional diagonal, by both containments, at "
         "n = 2,3,4",
         "the two halves together leave dimension one, and it is the scalar "
         "line, so the two controls decompose the forcing",
         "the upper containment is certified WITHOUT the solver -- every "
         "off-diagonal block is preserved and rigid -- so a solver that "
         "under-returns cannot be mistaken for a smaller invariant space",
         "the ambient is pinned set-exactly to the full n^2-dimensional "
         "Hermitian space, since 'exactly the diagonal' is weaker on a "
         "smaller ambient",
         "the phase half must be order-four quarter-phases on distinct "
         "coordinates, not order-two sign flips, which leave the same space",
         "the enumeration must find at least one non-scalar line",
         "on a 2-dimensional graded space a non-scalar PSD trace-2 invariant "
         "survives, so the dimension pin is load-bearing",),
        ('T_presentation_gauge_forces_trace',
         'T_closed_loop_score_is_normalized_trace'),
    )


# ==========================================================================
# LEG 2 -- the forcing theorem.
# ==========================================================================

def check_T_presentation_gauge_forces_trace() -> Dict[str, object]:
    """Tier 4, [P_structural | P1 open, P2 gauge, P3 underived]."""
    fails: List[str] = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)

    # ---- Step 3: the effects separate the Hermitian space. ----------------
    effect_ranks = {}
    for n in (2, 3, 4):
        basis = _herm_basis(n)
        rows = []
        for e in _effects(n):
            rows.append([_tr(_mm(b, e))[0] for b in basis])
        r = _rank(rows)
        effect_ranks[n] = r
        ck(r == n * n,
           f"Step 3 needs the effects to span Herm({n}) (rank {r}, want {n*n})")

    # ---- Step 4: the constraint map has rank n^2 - 1, nullity 1. ----------
    ranks = {}
    for n in (2, 3, 4, 5):
        basis = _herm_basis(n)
        gens = _complex_generators(n)
        dim = len(basis)
        cols = []
        for k in range(dim):
            col = []
            for g in gens:
                Mk = _mm(_mm(g, basis[k]), _dag(g))
                for a in range(n):
                    for b in range(n):
                        col.append(Mk[a][b][0] - basis[k][a][b][0])
                        col.append(Mk[a][b][1] - basis[k][a][b][1])
            cols.append(col)
        rows = [[cols[k][r] for k in range(dim)] for r in range(len(cols[0]))]
        rk = _rank(rows)
        ranks[n] = {"dim_herm": dim, "constraint_rank": rk, "nullity": dim - rk}
        ck(rk == dim - 1,
           f"Step 4 constraint rank must be n^2-1 at n={n} (got {rk} of {dim})")
        sols = _nullspace(rows, dim)
        ck(len(sols) == 1, f"Step 4 nullity must be 1 at n={n}")

    # ---- The conclusion: with psi = c*Tr the score IS Born. ---------------
    born_matches = 0
    for n in (2, 3):
        for c in (F(1), F(7, 3), F(-2)):          # c cancels, including c < 0
            R = _scale(c, _eye(n))
            b = [[(F(i + 1), F(0)) if j <= i else ZERO for j in range(n)]
                 for i in range(n)]
            h = _mm(b, _dag(b))
            for e in _effects(n):
                s, bn = _score(R, b, e), _born(h, e)
                ck(s is not None and s == bn,
                   f"psi = c*Tr must give the Born score (n={n}, c={c})")
                born_matches += 1
    ck(born_matches > 0, "ANTI-VACUITY: the Born-agreement battery must be non-empty")

    # ---- RESTRICTION (a): FALSE on a direct sum. -------------------------
    # M2 + M2 with R = 1*I + 3*I.  Block-diagonal unitaries never mix blocks,
    # so the per-block constants are fixed independently and do not cancel.
    Rb = _zeros(4)
    for i in range(2):
        Rb[i][i] = ONE
    for i in range(2, 4):
        Rb[i][i] = (F(3), F(0))
    b4 = _eye(4)
    h4 = _mm(b4, _dag(b4))
    e22 = _zeros(4)
    e22[2][2] = ONE
    s_blk, b_blk = _score(Rb, b4, e22), _born(h4, e22)
    ck(_is_psd(Rb, 4), "the direct-sum witness must be PSD (every premise holds)")
    ck(_tr(Rb) != ZERO, "the direct-sum witness must satisfy P4")
    ck(s_blk is not None and b_blk is not None and s_blk != b_blk,
       "RESTRICTION (a): the direct-sum witness must BREAK Born -- if this "
       "passes, the single-block fence is not load-bearing")
    # and it really is carrier-independent across the block-unitary family
    blk_invariant = True
    for g1 in _complex_generators(2):
        U = _zeros(4)
        for a in range(2):
            for b in range(2):
                U[a][b] = g1[a][b]
                U[a + 2][b + 2] = g1[a][b]
        s2 = _score(Rb, _mm(b4, U), e22)
        if s2 != s_blk:
            blk_invariant = False
    ck(blk_invariant,
       "RESTRICTION (a): the direct-sum witness must be genuinely "
       "carrier-independent, or it is not a counterexample to the hypothesis")

    # ---- RESTRICTION (b) + THE GAUGE-SENSE RULING. -----------------------
    # The trace-zero weight diag(1,-1).  Under the SUBGROUP reading it is
    # invariant and P4 is what excludes it.  Under the FULL-FIBRE reading --
    # the one this theorem is stated under -- it is NOT invariant at all.
    Rz = [[ONE, ZERO], [ZERO, (F(-1), F(0))]]
    ck(_tr(Rz) == ZERO, "the trace-zero witness must have Tr R = 0 (P4 excludes it)")
    ck(not _is_psd(Rz, 2), "the trace-zero witness must fail positivity")

    # subgroup reading: invariant under the named generators
    bz = [[(F(1), F(0)), (F(2), F(0))], [(F(3), F(0)), (F(5), F(0))]]
    e00 = [[ONE, ZERO], [ZERO, ZERO]]
    s_base = _score(Rz, bz, e00)
    sub_invariant = True
    for g in _complex_generators(2):
        if _score(Rz, _mm(bz, g), e00) != s_base:
            sub_invariant = False
    ck(sub_invariant,
       "SUBGROUP READING: the trace-zero witness must be invariant under the "
       "named generator families -- this is why it is a live failure mode when "
       "only a proper subgroup of presentations is realizable")

    # full-fibre reading: an exactly rational rotation breaks it
    U345 = [[(F(3, 5), F(0)), (F(-4, 5), F(0))],
            [(F(4, 5), F(0)), (F(3, 5), F(0))]]
    ck(_mm(_dag(U345), U345) == _eye(2), "the fibre probe must be exactly unitary")
    bzU = _mm(bz, U345)
    ck(_mm(bz, _dag(bz)) == _mm(bzU, _dag(bzU)),
       "the fibre probe must preserve the load h = b b*")
    s_fibre = _score(Rz, bzU, e00)
    ck(s_base is not None and s_fibre is not None and s_base != s_fibre,
       "FULL-FIBRE READING (the banked sense): the trace-zero witness must FAIL "
       "load-invariance across the right-unitary fibre -- so it does NOT satisfy "
       "this theorem's hypothesis and is excluded by the symmetry alone")
    born_z = _born(_mm(bz, _dag(bz)), e00)
    ck(s_base is not None and born_z is not None and s_base != born_z,
       "RESTRICTION (b): the subgroup-surviving weight must actually give a "
       "NON-BORN score, or the named failure mode is empty")

    # ---- RESTRICTION (b2): the sharper failure mode. ----------------------
    # P4 does NOT protect reading (ii) at an arbitrary realizable subgroup.
    # Two survivors on which P4 and positivity BOTH hold and the score is still
    # non-Born.  Computed, not asserted; each is checked to be (1) invariant
    # across its own subgroup orbit, so it satisfies (ii); (2) PSD with nonzero
    # trace, so neither premise reaches it; (3) non-Born; and (4) EXCLUDED by
    # the admitted family, which is what actually does the work.
    U345_ = [[(F(3, 5), F(0)), (F(-4, 5), F(0))],
             [(F(4, 5), F(0)), (F(3, 5), F(0))]]
    sharper = {}
    for tag, Rw, bw, sub in (
            ("sigma_x / transpositions",
             [[ONE, (F(1, 2), F(0))], [(F(1, 2), F(0)), ONE]],
             [[ONE, (F(2), F(0))], [(F(3), F(0)), (F(5), F(0))]],
             _transpositions(2)),
            ("sigma_y / rotation",
             [[ONE, (F(0), F(-1) / 2)], [(F(0), F(1) / 2), ONE]],
             [[ONE, (F(0), F(1))], [(F(3), F(0)), (F(5), F(0))]],
             [U345_])):
        ck(all(_mm(_mm(g, Rw), _dag(g)) == Rw for g in sub),
           "RESTRICTION (b2): the survivor must be invariant under its own "
           "realizable subgroup, or it does not satisfy reading (ii) [%s]" % tag)
        ck(_is_psd(Rw, 2) and _tr(Rw) != ZERO,
           "RESTRICTION (b2): and it must be PSD with NONZERO trace, or P4 or "
           "positivity would already exclude it [%s]" % tag)
        s_sub = _score(Rw, bw, e00)
        b_sub = _born(_mm(bw, _dag(bw)), e00)
        orbit = {_score(Rw, _mm(bw, g), e00) for g in sub} | {s_sub}
        ck(len(orbit) == 1,
           "RESTRICTION (b2): the score must be CONSTANT across the subgroup "
           "orbit, or the survivor is not (ii)-invariant as a score [%s]" % tag)
        ck(s_sub is not None and b_sub is not None and s_sub != b_sub,
           "RESTRICTION (b2): and the score must be NON-BORN, or there is no "
           "failure mode to name [%s]" % tag)
        ck(any(_mm(_mm(g, Rw), _dag(g)) != Rw for g in _complex_generators(2)),
           "RESTRICTION (b2): and the ADMITTED family must exclude it -- that is "
           "what protects the theorem, not P4 [%s]" % tag)
        sharper[tag] = {"score": str(s_sub), "born": str(b_sub),
                        "psd": True, "trace_re": str(_tr(Rw)[0])}

    # ---- P3 is load-bearing: at rank one the requirement is vacuous. ------
    rank_one_vacuous = True
    b_r1 = [[ONE, ZERO], [ZERO, ZERO]]
    for Rw in ([[ONE, ZERO], [ZERO, (F(5), F(0))]],
               [[(F(2), F(0)), ZERO], [ZERO, (F(7), F(0))]]):
        base = _score(Rw, b_r1, e00)
        for g in _complex_generators(2):
            s = _score(Rw, _mm(b_r1, g), e00)
            if s is not None and base is not None and s != base:
                rank_one_vacuous = False
    ck(rank_one_vacuous,
       "P3 load-bearing: at rank one the sandwich must be invariant for EVERY "
       "weight, so the content of the requirement lives on full-support loads")

    # ---- positivity is the SEPARATE c > 0 clause, not the forcing premise --
    c_positive = []
    for c in (F(1), F(7, 3)):
        R = _scale(c, _eye(2))
        c_positive.append(_is_psd(R, 2) and c > 0)
    ck(all(c_positive), "positivity must deliver c > 0 on the scalar line")
    R_neg = _scale(F(-2), _eye(2))
    ck(not _is_psd(R_neg, 2),
       "psi = -Tr must fail positivity (it is excluded by the SIGN clause only)")
    b_t = [[ONE, (F(2), F(0))], [(F(3), F(0)), (F(5), F(0))]]
    ck(_score(R_neg, b_t, e00) == _born(_mm(b_t, _dag(b_t)), e00),
       "psi = -Tr must still reproduce Born (c cancels) -- so the SIGN is not "
       "load-bearing for the conclusion, which is why positivity is not the "
       "forcing premise")

    key = (
        "SINGLE BLOCK M_n(C), premises P1 (sandwich realization, ALREADY OPEN in "
        "the corpus, not discharged here) + P2 (the load is the physical datum, "
        "the carrier is notation -- THE GAUGE ASSUMPTION, a claim about nature, "
        "renamed not removed) + P3 (the full-support load is admissible, "
        "underived, load-bearing) + P4 (psi(I) = Tr R != 0): if the score is a "
        "function of the LOAD then psi = c*Tr, c cancels, and eta_b(e) = "
        "Tr(rho_b e) with rho_b = b b*/Tr(b b*). Positivity is a SEPARATE clause "
        "buying c > 0 ONLY -- the forcing runs on P4, and psi = -Tr reproduces "
        "Born exactly (computed), so the sign is not load-bearing. THE PREMISE "
        "CORRECTION OF RECORD: the earlier 'excluded by positivity and by nothing "
        "weaker' is FALSE -- L_presentation_gauge_invariant_lines computes that "
        "every non-scalar invariant line has trace zero, so P4 suffices and is "
        "strictly weaker. THE GAUGE-SENSE RULING OF RECORD: banked under the "
        "FULL-FIBRE reading (invariance across {bU : U in U(n)}), which is what "
        "Step 1 and Step 2's b = I actually use; under it the trace-zero weight "
        "diag(1,-1) DOES NOT satisfy the hypothesis (computed: same load "
        "[[5,13],[13,34]], eta_b(E00) = 3/19 vs eta_bU(E00) = 9/73) and is "
        "excluded by symmetry alone. The SUBGROUP reading -- only some "
        "presentations realizable -- is carried as the sharpest NAMED FAILURE "
        "MODE: there the theorem returns a non-tracial functional and a non-Born "
        "score. TWO RESTRICTIONS, both executed: the conclusion is FALSE on a "
        "direct sum (M2+M2, R = I+3I: PSD, P4 satisfied, carrier-independent "
        "across the block-unitary family, score 3/8 vs Born 1/4), and P4 cannot "
        "be dropped (at Tr R = 0 the score at b = I is 0/0). Step 4 constraint "
        "rank n^2-1 / nullity 1 at n = 2,3,4,5. NOT a derivation of Born, NOT a "
        "derivation of the trace from A1 -- P1 is an open gate and P2 is a claim "
        "about nature."
    )
    return _result(
        'T_presentation_gauge_forces_trace',
        ('P_structural | P1 open (DAGGER_SANDWICH_REALIZATION / '
         'ROOTLESS_LOOP_CYCLICITY, named-open in operational_score_linearity), '
         'P2 gauge (the load is the physical datum -- a claim about nature, the '
         'premise an opponent denies), P3 underived (full-support admissibility). '
         'The forcing itself is exact finite mathematics; the grade is structural '
         'because three of its four premises are supplied, not proved'),
        key,
        {
            "effect_spanning_rank": effect_ranks,
            "step4_constraint_ranks": ranks,
            "born_agreement_cases": born_matches,
            "direct_sum_score": str(s_blk),
            "direct_sum_born": str(b_blk),
            "direct_sum_carrier_independent": blk_invariant,
            "trace_zero_subgroup_invariant": sub_invariant,
            "trace_zero_score_base": str(s_base),
            "trace_zero_score_after_fibre_rotation": str(s_fibre),
            "trace_zero_born": str(born_z),
            "trace_zero_full_fibre_invariant": (s_base == s_fibre),
            "subgroup_survivors_p4_and_positivity_hold": sharper,
            "rank_one_requirement_vacuous": rank_one_vacuous,
            "gauge_sense_banked": "full right-unitary fibre",
            "gauge_sense_named_failure_mode": "proper realizable subgroup",
        },
        fails,
        4,
        ('A1', 'L_epsilon*', 'L_presentation_gauge_invariant_lines'),
        ('SANDWICH_SCORE_REALIZATION_P1_OPEN',
         'LOAD_IS_THE_PHYSICAL_DATUM_P2_GAUGE',
         'FULL_SUPPORT_LOAD_ADMISSIBLE_P3',
         'PSI_OF_IDENTITY_NONZERO_P4',
         'LINEAR_REALIZATION_INHERITED'),
        ("direct sum M2+M2 breaks the conclusion",
         "trace-zero weight breaks it under the subgroup reading",
         "rank-one loads make the requirement vacuous",
         "psi = -Tr still reproduces Born (the sign is not load-bearing)",
         "two subgroup survivors on which P4 AND positivity hold and the score "
         "is non-Born -- the admitted family, not P4, is what excludes them"),
        ('T_closed_loop_score_is_normalized_trace',
         'L_gauge_forcing_supersedes_cyclicity_premise',
         'T_g_hold_exact_not_in_born_ancestry'),
    )


# ==========================================================================
# LEG 3 -- the prior-art relation: cyclicity derived, not assumed.
# ==========================================================================

def check_L_gauge_forcing_supersedes_cyclicity_premise() -> Dict[str, object]:
    """Tier 4, [P_structural_reading].  Same conclusion, strictly weaker premises."""
    fails: List[str] = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)

    # ---- live bank anchor: the prior art, and what it assumes -------------
    try:
        from apf.dense_sandwich_born import (
            check_T_closed_loop_score_is_normalized_trace as prior,
        )
        r_prior = prior()
    except Exception as exc:                                # pragma: no cover
        r_prior = {}
        fails.append(f"prior-art anchor could not be loaded: {exc!r}")

    prior_premises = tuple(r_prior.get('premises', ()))
    ck(r_prior.get('passed') is True,
       "anchor T_closed_loop_score_is_normalized_trace must pass live")
    ck('CLOSED_LOOP_SCORE_CYCLICITY' in prior_premises,
       "PRIOR-ART GATE: the anchor must actually carry cyclicity as a NAMED "
       "PREMISE -- if it stops doing so, this supersession claim is void and "
       "must be re-derived, not silently retained")

    # ---- our premise set does NOT contain cyclicity ----------------------
    ours = check_T_presentation_gauge_forces_trace()
    our_premises = tuple(ours.get('premises', ()))
    ck(ours.get('passed') is True, "the forcing theorem must pass")
    ck(not any('CYCLIC' in p.upper() for p in our_premises),
       "the forcing theorem must NOT assume cyclicity")

    # ---- cyclicity FALLS OUT of the conclusion, computed -----------------
    cyclic_pairs = 0
    for n in (2, 3):
        basis = _herm_basis(n)
        R = _scale(F(5, 2), _eye(n))          # any c on the forced line
        for a in basis:
            for b in basis:
                lhs = _tr(_mm(R, _mm(a, b)))
                rhs = _tr(_mm(R, _mm(b, a)))
                ck(lhs == rhs,
                   f"cyclicity must FOLLOW from psi = c*Tr (n={n})")
                cyclic_pairs += 1
    ck(cyclic_pairs > 0, "ANTI-VACUITY: the cyclicity battery must be non-empty")

    # ---- negative control: a non-tracial normalized score is NOT cyclic ---
    # The coordinate score L(a) = a[0][0] is normalized but not cyclic, so the
    # cyclicity battery has real discriminating power.
    E12 = [[ZERO, ONE], [ZERO, ZERO]]
    E21 = [[ZERO, ZERO], [ONE, ZERO]]
    coord_left = _mm(E12, E21)[0][0]
    coord_right = _mm(E21, E12)[0][0]
    ck(coord_left != coord_right,
       "NEGATIVE CONTROL: the normalized coordinate score must fail cyclicity, "
       "or the cyclicity battery proves nothing")

    key = (
        "THE SUPERSESSION, stated against live bank state. The banked "
        "T_closed_loop_score_is_normalized_trace (dense_sandwich_born.py) reaches "
        "psi = Tr/2 on M2(C) from linearity + CYCLICITY + normalization, with "
        "CLOSED_LOOP_SCORE_CYCLICITY a NAMED PREMISE (gated live in this check: "
        "if the anchor ever drops it, this claim voids). T_presentation_gauge_"
        "forces_trace reaches the SAME conclusion at GENERAL n from linearity + "
        "PRESENTATION GAUGE + psi(I) != 0, and does NOT assume cyclicity -- "
        "cyclicity is DERIVED, computed here over the full Hermitian basis at "
        "n = 2,3 from psi = c*Tr. So the premise set is strictly weaker on the "
        "load-bearing axis and the statement is strictly more general. WHAT THIS "
        "IS NOT: it is not a stronger result about NATURE. The gauge premise P2 "
        "is a claim about which object is physical, and it is not cheaper than "
        "cyclicity -- it is better SITED (at the ontology rather than at the "
        "group action) and it makes the opponent's position explicit. Reading "
        "grade for exactly that reason: the comparison of premise sets is "
        "computed, but 'better sited' is a judgement, not a theorem. Negative "
        "control: the normalized coordinate score is non-cyclic, so the "
        "cyclicity battery discriminates."
    )
    return _result(
        'L_gauge_forcing_supersedes_cyclicity_premise',
        ('P_structural_reading -- the premise-set comparison and the derived '
         'cyclicity are computed; the claim that gauge is BETTER SITED than '
         'cyclicity is a judgement about premise quality, not a theorem, and is '
         'graded accordingly'),
        key,
        {
            "prior_art_check": 'T_closed_loop_score_is_normalized_trace',
            "prior_art_module": 'dense_sandwich_born.py',
            "prior_art_premises": list(prior_premises),
            "prior_art_assumes_cyclicity": 'CLOSED_LOOP_SCORE_CYCLICITY' in prior_premises,
            "our_premises": list(our_premises),
            "our_premises_assume_cyclicity": any('CYCLIC' in p.upper()
                                                 for p in our_premises),
            "cyclicity_pairs_derived": cyclic_pairs,
            "prior_art_scope": 'n = 2',
            "this_scope": 'general n (executed at n = 2,3,4,5)',
        },
        fails,
        4,
        ('T_presentation_gauge_forces_trace',
         'T_closed_loop_score_is_normalized_trace'),
        ('LOAD_IS_THE_PHYSICAL_DATUM_P2_GAUGE',),
        ("the normalized coordinate score must fail cyclicity",
         "the anchor must still carry cyclicity as a named premise",),
        ('L_presentation_gauge_invariant_lines',),
    )


_CHECKS = {
    'L_presentation_gauge_invariant_lines': check_L_presentation_gauge_invariant_lines,
    'T_presentation_gauge_forces_trace': check_T_presentation_gauge_forces_trace,
    'L_gauge_forcing_supersedes_cyclicity_premise':
        check_L_gauge_forcing_supersedes_cyclicity_premise,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == '__main__':
    import sys
    bad = False
    for n, fn in _CHECKS.items():
        r = fn()
        print(r['name'], '::', r['epistemic'][:64], '::',
              'PASS' if r['passed'] else 'FAIL')
        if not r['passed']:
            bad = True
            for f in r['fail_reasons']:
                print('  -', f)
    sys.exit(1 if bad else 0)
