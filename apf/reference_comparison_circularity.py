"""The symmetric-reference comparison route to the preparation load is circular.

Staged 2026-07-29 (v24.3.455 slot) and held pending audits per the standing
rule that an audit of a source packet is not an audit of the code that enters
the bank.

AUDIT RECORD: blinded cold LAND-WITH-FIXES 0.82 (2026-07-29, statement + code
only, no lineage; the identity verified independently over a full basis of
M_n(C) at n = 2..5 in exact Gaussian-rational arithmetic, 0 counterexamples)
+ LAND-WITH-FIXES 0.84 (2026-08-04, D1-queue blinded cold audit; the uncarried
.455-owed fixes carried by a separate fix seat, auditor's escapes re-run) +
LAND-WITH-FIXES 0.88 (2026-08-04, third blinded cold audit, zero MAJORs, all
arithmetic reproduced independently in exact sympy with zero disagreements;
both owed fixes carried the same day by a separate cold fix seat -- the
tautological leg all_state_witnesses_used deleted, a value-tie leg added
asserting det(P_b) = 5/72 exactly by cofactor expansion, a routine separate
from the rank's Gaussian elimination; auditor's battery re-run post-fix, M15
now caught by the det leg, the proven true invariances M05/M06/M26/M29 and
M10b still escape -- the residual disclosed in the _result docstring).
Fixes carried by separate cold fix seats each round.  Banked as v24.3.466
(2026-08-04).

WHAT THIS ADDS, AGAINST THE PRIOR ART (read this first).

P2 of check_T_presentation_gauge_forces_trace (presentation_gauge_forcing.py,
v24.3.443) -- that the LOAD is the physical datum -- is banked as a claim about
nature, the premise an opponent denies.  One proposed discharge compares a
physical same-preparation reference against a claimed load-built reference and
argues that agreement forces the preparation-load identity.

IT IS CIRCULAR, and this module computes why.

  A physical same-preparation symmetric reference induces, on the comparator,
  the effect built from the OPERATIONAL STATE:

      Tr_R[(I (x) rho) (I + SWAP)/2]  =  (Tr(rho) I + rho)/2  =  (I + rho)/2.

  The route needs it to be the effect built from the LOAD, (I + P_b)/2 with
  P_b = b b* / Tr(b b*).  Those two effects are equal if and only if
  rho = P_b -- which is the preparation-load identity itself.  So the
  comparison does not derive the identity; it presupposes it.

  THE SUBSTITUTION IS THE ASSUMPTION, computed: feeding the comparator the load
  P_b in place of the operational state rho returns the claimed effect by
  construction.  That substitution is exactly the step the route needs to
  justify.

A SECOND CORRECTION, smaller and worth recording.  The source derivation writes
the induced effect as (I + rho^T)/2 and then reconciles it "with the usual
conjugate convention."  There is no transpose to reconcile: the standard partial
trace identity Tr_2[(A (x) B) SWAP] = A B gives (Tr(rho) I + rho)/2 directly,
with no conjugation anywhere.  Computed here against an ASYMMETRIC trace-zero
probe, which is the only kind of witness that can tell the two apart -- on any
symmetric or real probe the alleged transpose is invisible.  The reconciliation
papered over an error that was not there, in the load-bearing display of the
argument.

============================================================================
STATEMENTS

check_L_symmetric_reference_comparison_is_circular
(tier 3, [P_math]).

  (a) THE INDUCED EFFECT, computed exactly on genuinely complex unit-trace
      states at n = 2 and n = 3: Tr_R[(I (x) rho) Pi_sym] = (Tr(rho) I + rho)/2.
      The symmetric projector is BUILT from an explicitly constructed SWAP and
      verified idempotent and Hermitian, not assumed.

  (b) NO TRANSPOSE, and the witness is the point: on the ASYMMETRIC trace-zero
      probe A = E_01 the comparator returns A/2 and NOT A^T/2, which differ.  A
      symmetric or real probe cannot distinguish them, so the leg asserts the
      probe is asymmetric before using it.

  (c) THE CIRCULARITY, both directions computed.  For an exhibited pair
      (rho, P_b) with rho != P_b -- both genuine unit-trace PSD states -- the
      two induced effects DIFFER; and with rho = P_b they COINCIDE: feeding
      the load P_b to the comparator in place of the operational state returns
      (I + P_b)/2 by construction, which is exactly the substitution the route
      performs silently.  One computation carries both readings, so it is one
      leg.  Together with (f), "the two references agree" is EQUIVALENT to the
      preparation-load identity, not evidence for it.

  (d) SCOPE, executed: the load P_b = b b*/Tr(b b*) is verified a genuine
      unit-trace PSD state, its rank is COMPUTED by exact Gaussian
      elimination (rank(P_b) = 2), and det(P_b) = 5/72 is asserted exactly,
      computed by cofactor expansion -- a routine separate from the
      elimination (det(b b*) = 10 != 0; the eigenvalues are
      1/2 +- sqrt(26)/12).  The circularity is not an artifact of a
      malformed load, and the load is full-rank, not a ray.

  (e) FAIL-CONTROLS for the PSD guard, computed by value: two Hermitian
      unit-trace NON-PSD matrices -- diag(2, 0, -1), whose leading principal
      minors are all non-negative while a 1x1 principal minor is negative and
      whose determinant is 0 >= 0, and [[1/2, i], [-i, 1/2]], whose only
      negative principal minor is the full determinant -3/4 -- are fed to the
      guard, and its False verdict on each is asserted.

  (f) THE COMPARATOR IDENTITY, SYMBOLIC, and affine injectivity.  Over formal
      Gaussian-rational matrix entries at n = 2 and n = 3, the comparator
      pipeline returns exactly (Tr(Z) I + Z)/2 as a polynomial identity in the
      entries, and the symbolic result evaluated at the numeric witnesses
      agrees with the numeric comparator entry-for-entry.  The difference
      identity eff(Z) - eff(W) = ((Tr Z - Tr W) I + (Z - W))/2 is computed the
      same way; on unit-trace states it is (Z - W)/2, which vanishes only at
      Z = W.  This is the forward direction of the equivalence in (c).

============================================================================
MAY-NOT-CITE.

  - "The preparation-load identity is refuted", or "rho_b != P_b."  NOT SHOWN.
    This kills one ROUTE to the identity.  The identity may well hold; what
    fails is this argument for it.
  - "P2 is discharged", or "P2 is refuted."  Neither.  P2 stays exactly where
    the bank has it: a claim about nature.
  - "Born is derived" or "Born is refuted."  Nothing here touches Born.
  - "The symmetric reference is unphysical."  Not claimed.  The reference is
    fine; the inference from it is what fails.
  - "All reference-comparison routes are circular."  Only the same-preparation
    symmetric one computed here.

PROVENANCE.  The circularity finding is from the external packet
APF_ATOMIC_PREPARATION_READOUT_RECIPROCITY_AUDIT v0.8 (2026-07-29), where it
appears as a self-kill of that lane's own v0.7 route -- the packet retracted its
own prior proposal, which is the reason this one item was worth carrying when
the rest of that packet reduced.  A blinded cold audit attacked the kill two
ways (a transpose countermodel, and feeding the carrier to the comparator) and
could not break it.  The transpose correction in the source's displayed
derivation is recorded here because that audit found it.

NON-EXPORTING.  physical_premises_certified = false.  No existing grade moved.
"""

from fractions import Fraction as F
from typing import Dict, List, Tuple

PHYSICAL_PREMISES_CERTIFIED = False
EXPORTS: Tuple[str, ...] = ()
BANK_MODIFIED = False

G = Tuple[F, F]
Mat = List[List[G]]

ZERO: G = (F(0), F(0))
ONE: G = (F(1), F(0))
HALF: G = (F(1, 2), F(0))
MINUS_ONE: G = (F(-1), F(0))


def _g(re, im=0) -> G:
    return (F(re), F(im))


def _add(a: G, b: G) -> G:
    return (a[0] + b[0], a[1] + b[1])


def _sub(a: G, b: G) -> G:
    return (a[0] - b[0], a[1] - b[1])


def _mul(a: G, b: G) -> G:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def _sc(k: F, a: G) -> G:
    return (k * a[0], k * a[1])


def _conj(a: G) -> G:
    return (a[0], -a[1])


def _inv_g(a: G) -> G:
    d = a[0] * a[0] + a[1] * a[1]
    return (a[0] / d, -a[1] / d)


def _zeros(n: int, m: int = None) -> Mat:
    m = n if m is None else m
    return [[ZERO] * m for _ in range(n)]


def _eye(n: int) -> Mat:
    M = _zeros(n)
    for i in range(n):
        M[i][i] = ONE
    return M


def _mm(A: Mat, B: Mat) -> Mat:
    n, k, m = len(A), len(B), len(B[0])
    out = _zeros(n, m)
    for i in range(n):
        for j in range(m):
            acc = ZERO
            for t in range(k):
                acc = _add(acc, _mul(A[i][t], B[t][j]))
            out[i][j] = acc
    return out


def _dag(A: Mat) -> Mat:
    return [[_conj(A[i][j]) for i in range(len(A))] for j in range(len(A[0]))]


def _transpose(A: Mat) -> Mat:
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def _tr(A: Mat) -> G:
    acc = ZERO
    for i in range(len(A)):
        acc = _add(acc, A[i][i])
    return acc


def _scale(k: F, A: Mat) -> Mat:
    return [[_sc(k, x) for x in row] for row in A]


def _plus(A: Mat, B: Mat) -> Mat:
    return [[_add(a, b) for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]


def _swap(n: int) -> Mat:
    """S|a,b> = |b,a> on C^n (x) C^n, built explicitly."""
    S = _zeros(n * n)
    for a in range(n):
        for b in range(n):
            S[a * n + b][b * n + a] = ONE
    return S


def _kron(A: Mat, B: Mat) -> Mat:
    n, m = len(A), len(B)
    out = _zeros(n * m)
    for i in range(n):
        for j in range(n):
            for k in range(m):
                for l in range(m):
                    out[i * m + k][j * m + l] = _mul(A[i][j], B[k][l])
    return out


def _partial_trace_second(M: Mat, n: int) -> Mat:
    """Tr_2 over the SECOND tensor factor of C^n (x) C^n."""
    out = _zeros(n)
    for i in range(n):
        for j in range(n):
            acc = ZERO
            for k in range(n):
                acc = _add(acc, M[i * n + k][j * n + k])
            out[i][j] = acc
    return out


def _comparator(rho: Mat, n: int) -> Mat:
    """The effect a same-preparation symmetric reference induces:
    Tr_2[(I (x) rho) (I + SWAP)/2]."""
    big = _kron(_eye(n), rho)
    pi_sym = _scale(F(1, 2), _plus(_eye(n * n), _swap(n)))
    return _partial_trace_second(_mm(big, pi_sym), n)


def _is_psd_unit_trace(rho: Mat, n: int) -> bool:
    """Hermitian, unit trace, and PSD via ALL principal minors (exact).

    For a Hermitian matrix, PSD is checked here by requiring every principal
    minor of every order to be non-negative, which is exact and sufficient."""
    if _tr(rho) != ONE:
        return False
    if _dag(rho) != rho:
        return False
    from itertools import combinations
    for k in range(1, n + 1):
        for idx in combinations(range(n), k):
            sub = [[rho[i][j] for j in idx] for i in idx]
            d = _det(sub)
            if d[1] != F(0) or d[0] < F(0):
                return False
    return True


def _det(M: Mat) -> G:
    n = len(M)
    if n == 1:
        return M[0][0]
    acc = ZERO
    for j in range(n):
        minor = [[M[i][c] for c in range(n) if c != j] for i in range(1, n)]
        term = _mul(M[0][j], _det(minor))
        acc = _add(acc, term) if j % 2 == 0 else _sub(acc, term)
    return acc


def _fmt_g(x: G) -> str:
    """Render a Gaussian rational for evidence strings; a negative imaginary
    part prints as '-' rather than '+-'."""
    if x[1] == F(0):
        return str(x[0])
    sign = '+' if x[1] > 0 else '-'
    return f"{x[0]}{sign}{abs(x[1])}i"


def _rank(M: Mat) -> int:
    """Rank over the Gaussian rationals, by exact Gaussian elimination."""
    A = [row[:] for row in M]
    rows, cols = len(A), len(A[0])
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i][c] != ZERO), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = _inv_g(A[r][c])
        A[r] = [_mul(inv, x) for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c] != ZERO:
                f = A[i][c]
                A[i] = [_sub(x, _mul(f, y)) for x, y in zip(A[i], A[r])]
        r += 1
        if r == rows:
            break
    return r


# ---------------------------------------------------------------------------
# Formal (symbolic) layer: matrix entries as linear forms over Q(i), so the
# comparator identity is computed as a POLYNOMIAL IDENTITY in the entries
# rather than at finitely many states.  A linear form is a dict mapping a
# variable name to its (exact, Gaussian-rational) complex coefficient; zero
# coefficients are pruned, so dict equality is equality of forms.
# ---------------------------------------------------------------------------

LF = Dict[str, G]


def _lf_var(name: str) -> LF:
    return {name: ONE}


def _lf_add(a: LF, b: LF) -> LF:
    out = dict(a)
    for k, v in b.items():
        s = _add(out.get(k, ZERO), v)
        if s == ZERO:
            out.pop(k, None)
        else:
            out[k] = s
    return out


def _lf_cmul(c: G, a: LF) -> LF:
    out: LF = {}
    if c == ZERO:
        return out
    for k, v in a.items():
        p = _mul(c, v)
        if p != ZERO:
            out[k] = p
    return out


def _lf_sub(a: LF, b: LF) -> LF:
    return _lf_add(a, _lf_cmul(MINUS_ONE, b))


def _lf_eval(a: LF, assign: Dict[str, G]) -> G:
    acc = ZERO
    for k, v in a.items():
        acc = _add(acc, _mul(v, assign[k]))
    return acc


def _sym_state(n: int, prefix: str) -> List[List[LF]]:
    return [[_lf_var(f"{prefix}_{i}_{j}") for j in range(n)] for i in range(n)]


def _sym_trace(Z: List[List[LF]], n: int) -> LF:
    acc: LF = {}
    for a in range(n):
        acc = _lf_add(acc, Z[a][a])
    return acc


def _sym_comparator(Z: List[List[LF]], n: int) -> List[List[LF]]:
    """The comparator pipeline on FORMAL entries: build kron(I, Z), multiply
    by the (constant, exact) symmetric projector, partial-trace the second
    factor.  Every step is the same arithmetic the numeric comparator does,
    carried on linear forms."""
    N = n * n
    big: List[List[LF]] = [[{} for _ in range(N)] for _ in range(N)]
    for i in range(n):
        for k in range(n):
            for l in range(n):
                big[i * n + k][i * n + l] = Z[k][l]
    pi = _scale(F(1, 2), _plus(_eye(N), _swap(n)))
    prod: List[List[LF]] = [[{} for _ in range(N)] for _ in range(N)]
    for r in range(N):
        for c in range(N):
            acc: LF = {}
            for t in range(N):
                if pi[t][c] != ZERO and big[r][t]:
                    acc = _lf_add(acc, _lf_cmul(pi[t][c], big[r][t]))
            prod[r][c] = acc
    out: List[List[LF]] = [[{} for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            acc = {}
            for k in range(n):
                acc = _lf_add(acc, prod[i * n + k][j * n + k])
            out[i][j] = acc
    return out


def _sym_target(Z: List[List[LF]], n: int) -> List[List[LF]]:
    """(Tr(Z) I + Z)/2 on formal entries."""
    tr = _sym_trace(Z, n)
    return [[_lf_cmul(HALF, _lf_add(Z[i][j], tr) if i == j else Z[i][j])
             for j in range(n)] for i in range(n)]


# The frozen leg inventory.  _result() asserts the multiset of executed leg
# labels equals this list exactly; a leg that did not run, ran twice, or ran
# under an unlisted label raises before any verdict is returned.
_EXPECTED_LEGS: Tuple[str, ...] = (
    'swap_involution_n2', 'swap_hermitian_n2',
    'proj_idempotent_n2', 'proj_hermitian_n2',
    'swap_involution_n3', 'swap_hermitian_n3',
    'proj_idempotent_n3', 'proj_hermitian_n3',
    'state_psd_qubit_complex', 'state_complex_qubit_complex',
    'induced_effect_qubit_complex',
    'state_psd_qutrit_complex', 'state_complex_qutrit_complex',
    'induced_effect_qutrit_complex',
    'probe_asymmetric', 'probe_traceless',
    'comparator_no_transpose', 'comparator_not_transpose_effect',
    'load_trace_real_positive', 'load_psd_unit_trace', 'load_rank_two',
    'load_det_value',
    'states_differ', 'effects_differ_when_states_differ',
    'effects_coincide_substitution',
    'psd_control_wellformed_zero_block_neg_eig',
    'psd_control_rejected_zero_block_neg_eig',
    'psd_control_wellformed_sign_sensitive_offdiag',
    'psd_control_rejected_sign_sensitive_offdiag',
    'sym_identity_n2', 'sym_matches_numeric_n2',
    'affine_difference_identity_n2',
    'sym_identity_n3', 'sym_matches_numeric_n3',
    'affine_difference_identity_n3',
)


def _result(name, epistemic, key_result, evidence, fails, tier,
            dependencies, premises, negative_controls, cross_refs,
            fail_count=None, executed_legs=None, expected_legs=None):
    """Build the result dict; CROSS-ASSERT the failure records and the leg
    inventory HERE, because the bank never calls run_all().

    Two enforcement clauses.  (1) The two failure records must agree.
    (2) When a frozen leg list is supplied, the MULTISET of executed leg
    labels must equal it exactly.  Disclosed residual limits: clause (1)
    catches DIVERGENCE between the two records, not a bare literal
    substitution of 'passed'; both records are written at the same site, so
    an edit removing both is not caught."""
    counted = len(fails) if fail_count is None else fail_count
    if len(fails) != counted:
        raise AssertionError(
            f"{name}: failure records disagree -- fail_reasons has "
            f"{len(fails)} entries, the independent counter says {counted}")
    if expected_legs is not None:
        got = sorted(executed_legs or ())
        exp = sorted(expected_legs)
        if got != exp:
            from collections import Counter
            cg, ce = Counter(got), Counter(exp)
            missing = sorted((ce - cg).elements())
            extra = sorted((cg - ce).elements())
            raise AssertionError(
                f"{name}: executed leg inventory does not equal the frozen "
                f"list -- missing {missing}, unexpected or duplicated "
                f"{extra}, executed {len(got)} vs expected {len(exp)}")
    return {
        'fail_count': counted,
        'name': name,
        'epistemic': epistemic,
        'passed': (counted == 0),
        'tier': tier,
        'key_result': key_result,
        'evidence': evidence,
        'fail_reasons': fails,
        'leg_count': len(executed_legs) if executed_legs is not None else None,
        'dependencies': list(dependencies),
        'premises': list(premises),
        'negative_controls': list(negative_controls),
        'cross_refs': list(cross_refs),
        'physical_premises_certified': PHYSICAL_PREMISES_CERTIFIED,
        'exports': list(EXPORTS),
        'bank_modified': BANK_MODIFIED,
    }


def check_L_symmetric_reference_comparison_is_circular() -> Dict[str, object]:
    """Tier 3, [P_math]."""
    fails: List[str] = []
    tally = [0]
    executed: List[str] = []
    dims_exercised = set()

    def ck(label, cond, msg):
        executed.append(label)
        if not cond:
            fails.append(f"[{label}] {msg}")
            tally[0] += 1

    # ---- The symmetric projector is BUILT and verified, not assumed. ----
    for n in (2, 3):
        S = _swap(n)
        ck(f'swap_involution_n{n}', _mm(S, S) == _eye(n * n),
           f"SWAP must be an involution (n={n})")
        ck(f'swap_hermitian_n{n}', _dag(S) == S,
           f"SWAP must be Hermitian (n={n})")
        pi = _scale(F(1, 2), _plus(_eye(n * n), S))
        ck(f'proj_idempotent_n{n}', _mm(pi, pi) == pi,
           f"the symmetric projector must be idempotent (n={n})")
        ck(f'proj_hermitian_n{n}', _dag(pi) == pi,
           f"the symmetric projector must be Hermitian (n={n})")

    # ---- (a) THE INDUCED EFFECT on genuinely complex unit-trace states. --
    states: Dict[str, Tuple[int, Mat]] = {
        "qubit_complex": (2, [[_g(F(3, 4)), _g(0, F(1, 4))],
                              [_g(0, F(-1, 4)), _g(F(1, 4))]]),
        "qutrit_complex": (3, [[_g(F(1, 2)), _g(0, F(1, 8)), _g(F(1, 8))],
                               [_g(0, F(-1, 8)), _g(F(1, 4)), _g(0)],
                               [_g(F(1, 8)), _g(0), _g(F(1, 4))]]),
    }
    for label, (n, rho) in states.items():
        ck(f'state_psd_{label}', _is_psd_unit_trace(rho, n),
           f"the witness {label} must be a genuine unit-trace PSD state")
        ck(f'state_complex_{label}',
           any(x[1] != F(0) for row in rho for x in row),
           f"the witness {label} must be GENUINELY COMPLEX, or the transpose "
           f"leg below cannot discriminate")
        got = _comparator(rho, n)
        dims_exercised.add(n)
        want = _scale(F(1, 2), _plus(_eye(n), rho))
        ck(f'induced_effect_{label}', got == want,
           f"the induced effect must be (I + rho)/2 exactly ({label})")

    # ---- (b) NO TRANSPOSE.  The probe must be ASYMMETRIC or this is idle. --
    probe: Mat = [[ZERO, ONE], [ZERO, ZERO]]          # E_01, trace zero
    probe_asym = _transpose(probe) != probe
    ck('probe_asymmetric', probe_asym,
       "the transpose probe must be ASYMMETRIC -- on a symmetric probe the "
       "alleged transpose is invisible and the leg proves nothing")
    ck('probe_traceless', _tr(probe) == ZERO,
       "the transpose probe is chosen trace-zero, so the Tr(rho) I term drops "
       "and the comparator isolates the second term")
    got_probe = _comparator(probe, 2)
    dims_exercised.add(2)
    want_no_transpose = _scale(F(1, 2), probe)
    want_with_transpose = _scale(F(1, 2), _transpose(probe))
    ck('comparator_no_transpose', got_probe == want_no_transpose,
       f"the comparator must return A/2 with NO transpose, got {got_probe}")
    ck('comparator_not_transpose_effect', got_probe != want_with_transpose,
       "and must DIFFER from A^T/2 -- if these agreed the probe would not "
       "discriminate and the source's 'conjugate convention' reconciliation "
       "could not be adjudicated either way")

    # ---- (d) THE LOAD is a genuine unit-trace state; its rank is COMPUTED
    # by exact Gaussian elimination (it is 2 -- det(b b*) = 10 != 0, so the
    # load is full-rank, not a ray). --------------------------------------
    b: Mat = [[_g(1, 1), _g(2)], [_g(0, 1), _g(-1, 2)]]
    load = _mm(b, _dag(b))
    tr_load = _tr(load)
    ck('load_trace_real_positive', tr_load[1] == F(0) and tr_load[0] > F(0),
       "the load Tr(b b*) must be real and positive")
    P_b = _scale(F(1) / tr_load[0], load)
    ck('load_psd_unit_trace', _is_psd_unit_trace(P_b, 2),
       "the normalized load must be a genuine unit-trace PSD state")
    load_rank = _rank(P_b)
    load_det = _det(P_b)
    ck('load_rank_two', load_rank == 2,
       f"the rank of P_b, computed by exact Gaussian elimination, must be 2 "
       f"(got {load_rank}; det(P_b) = {load_det})")
    ck('load_det_value', load_det == (F(5, 72), F(0)),
       f"det(P_b), computed by cofactor expansion -- a routine separate from "
       f"the elimination -- must equal 5/72 exactly (got {load_det})")

    # ---- (c) THE CIRCULARITY, both directions. --------------------------
    rho_other = states["qubit_complex"][1]
    ck('states_differ', rho_other != P_b,
       "the two states must actually differ, or the circularity leg is idle")
    eff_state = _comparator(rho_other, 2)
    dims_exercised.add(2)
    eff_load = _scale(F(1, 2), _plus(_eye(2), P_b))
    effects_differ = eff_state != eff_load
    ck('effects_differ_when_states_differ', effects_differ,
       "with rho != P_b the two induced effects must DIFFER -- this is the "
       "half showing the comparison has content only when the identity holds")
    # The converse: with rho = P_b they coincide.  This one computation is
    # also the substitution the route performs silently -- feeding the LOAD
    # to the comparator returns the claimed effect by construction, which is
    # precisely the step the route needs to justify and does not.
    sub_effect = _comparator(P_b, 2)
    dims_exercised.add(2)
    effects_coincide = sub_effect == eff_load
    ck('effects_coincide_substitution', effects_coincide,
       "with rho = P_b the two induced effects must COINCIDE: feeding the "
       "LOAD to the comparator returns (I + P_b)/2 by construction, the "
       "substitution the route performs silently -- so agreement is "
       "EQUIVALENT to the preparation-load identity, not evidence for it")

    # ---- (e) FAIL-CONTROLS: the PSD guard's False branch, by value. ------
    # diag(2, 0, -1): every LEADING principal minor is non-negative (2, 0, 0)
    # and det = 0 >= 0, while the 1x1 principal minor at index 2 is -1.
    # [[1/2, i], [-i, 1/2]]: 1x1 minors are 1/2, and the only negative
    # principal minor is the full determinant 1/4 - 1 = -3/4.
    controls: Dict[str, Tuple[int, Mat]] = {
        'zero_block_neg_eig': (3, [[_g(2), ZERO, ZERO],
                                   [ZERO, ZERO, ZERO],
                                   [ZERO, ZERO, _g(-1)]]),
        'sign_sensitive_offdiag': (2, [[_g(F(1, 2)), _g(0, 1)],
                                       [_g(0, -1), _g(F(1, 2))]]),
    }
    control_rejections: Dict[str, bool] = {}
    for lbl, (n, C) in controls.items():
        ck(f'psd_control_wellformed_{lbl}',
           _tr(C) == ONE and _dag(C) == C,
           f"the control {lbl} must be Hermitian with unit trace, so the "
           f"guard's verdict on it is about positivity alone")
        verdict = _is_psd_unit_trace(C, n)
        control_rejections[lbl] = verdict
        ck(f'psd_control_rejected_{lbl}', verdict is False,
           f"the PSD guard must return False on the non-PSD control {lbl}")

    # ---- (f) THE COMPARATOR IDENTITY on formal entries, and injectivity. -
    witness_by_n = {n: rho for (n, rho) in states.values()}
    sym_identity_holds: Dict[int, bool] = {}
    diff_identity_holds: Dict[int, bool] = {}
    for n in (2, 3):
        Zv = _sym_state(n, "z")
        eff_sym = _sym_comparator(Zv, n)
        dims_exercised.add(n)
        sym_identity_holds[n] = eff_sym == _sym_target(Zv, n)
        ck(f'sym_identity_n{n}', sym_identity_holds[n],
           f"the comparator on formal entries must equal (Tr(Z) I + Z)/2 as "
           f"a polynomial identity in the entries (n={n})")
        rho_n = witness_by_n[n]
        assign = {f"z_{i}_{j}": rho_n[i][j]
                  for i in range(n) for j in range(n)}
        sym_eval = [[_lf_eval(eff_sym[i][j], assign) for j in range(n)]
                    for i in range(n)]
        ck(f'sym_matches_numeric_n{n}', sym_eval == _comparator(rho_n, n),
           f"the symbolic comparator evaluated at the n={n} witness must "
           f"agree with the numeric comparator entry-for-entry")
        Wv = _sym_state(n, "w")
        eff_w = _sym_comparator(Wv, n)
        diff = [[_lf_sub(eff_sym[i][j], eff_w[i][j]) for j in range(n)]
                for i in range(n)]
        tr_diff = _lf_sub(_sym_trace(Zv, n), _sym_trace(Wv, n))
        want_diff = [[_lf_cmul(HALF,
                               _lf_add(_lf_sub(Zv[i][j], Wv[i][j]), tr_diff)
                               if i == j else _lf_sub(Zv[i][j], Wv[i][j]))
                      for j in range(n)] for i in range(n)]
        diff_identity_holds[n] = diff == want_diff
        ck(f'affine_difference_identity_n{n}', diff_identity_holds[n],
           f"eff(Z) - eff(W) must equal ((Tr Z - Tr W) I + (Z - W))/2 "
           f"identically in the entries (n={n}); on unit-trace states this "
           f"is (Z - W)/2, which vanishes only at Z = W, so agreement of the "
           f"induced effects forces the states equal")

    return _result(
        'L_symmetric_reference_comparison_is_circular',
        'P_math',
        ("THE SYMMETRIC-REFERENCE COMPARISON ROUTE TO THE PREPARATION LOAD IS "
         "CIRCULAR.  A same-preparation symmetric reference induces "
         "Tr_2[(I (x) rho)(I + SWAP)/2] = (Tr(rho) I + rho)/2 = (I + rho)/2, "
         "built from the OPERATIONAL STATE -- computed exactly on genuinely "
         "complex unit-trace states at n = 2 and 3, computed SYMBOLICALLY as "
         "a polynomial identity in formal Gaussian-rational matrix entries at "
         "the same dimensions, with the symmetric projector BUILT from an "
         "explicit SWAP and verified idempotent and Hermitian.  The route "
         "needs the effect built from the LOAD, (I + P_b)/2, where P_b is "
         "verified PSD unit-trace with COMPUTED rank 2 and det(P_b) = 5/72 "
         "asserted exactly.  BOTH DIRECTIONS ARE "
         "COMPUTED: with rho != P_b the two induced effects DIFFER; with "
         "rho = P_b they COINCIDE by construction, which is the substitution "
         "the route performs silently; and the symbolic difference identity "
         "eff(Z) - eff(W) = ((Tr Z - Tr W) I + (Z - W))/2 shows agreement of "
         "the induced effects on unit-trace states forces Z = W.  So 'the "
         "two references agree' is EQUIVALENT to the preparation-load "
         "identity rather than evidence for it.  A SECOND CORRECTION: the "
         "source derivation writes (I + rho^T)/2 and reconciles it 'with the "
         "usual conjugate convention'; there is no transpose -- computed "
         "against an ASYMMETRIC trace-zero probe, the only witness that can "
         "tell them apart, the comparator returns A/2 and not A^T/2.  MAY "
         "NOT BE CITED as refuting the preparation-load identity or as "
         "discharging or refuting P2: this kills one ROUTE, and the identity "
         "may well hold."),
        {
            'dimensions': sorted(dims_exercised),
            'state_witnesses': sorted(states),
            'load_trace': str(tr_load[0]),
            'load_rank': load_rank,
            'load_det': _fmt_g(load_det),
            'probe_is_asymmetric': probe_asym,
            'comparator_on_probe': [[_fmt_g(x) for x in row]
                                    for row in got_probe],
            'states_differ': rho_other != P_b,
            'effects_differ_when_states_differ': effects_differ,
            'effects_coincide_when_states_agree': effects_coincide,
            'nonpsd_controls_guard_verdicts': control_rejections,
            'symbolic_identity_holds': sym_identity_holds,
            'affine_difference_identity_holds': diff_identity_holds,
        },
        fails,
        3,
        (),
        ("MODELLING PREMISE -- comparator identification, both halves: the "
         "physical same-preparation symmetric reference is taken to induce "
         "on the comparator exactly the effect Tr_2[(I (x) rho) "
         "(I + SWAP)/2], and the route's claimed target is taken to be the "
         "effect built from the LOAD, (I + P_b)/2.  Every statement in this "
         "module is downstream of that identification.",
         "Downstream of the premise: exact finite mathematics over Gaussian "
         "rationals.  The PHYSICAL question -- whether the preparation-load "
         "identity in fact holds -- is untouched, and P2 stays a claim about "
         "nature.",),
        ("the transpose probe is asserted ASYMMETRIC, or the transpose "
         "correction could not be adjudicated",
         "the two states are asserted to differ, or the circularity leg is idle",
         "the load is verified a genuine unit-trace PSD state and its rank "
         "is computed by exact elimination",
         "every state witness is asserted genuinely complex",
         "two Hermitian unit-trace NON-PSD controls are fed to the PSD guard "
         "and its False verdict on each is asserted by value",),
        ('T_presentation_gauge_forces_trace (P2 -- untouched)',
         'L_purification_orbit_fibre',
         'L_identity_carrier_vectorization'),
        fail_count=tally[0],
        executed_legs=executed,
        expected_legs=_EXPECTED_LEGS,
    )


_CHECKS = {
    'L_symmetric_reference_comparison_is_circular':
        check_L_symmetric_reference_comparison_is_circular,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    """Second gate only; the load-bearing cross-asserts live in _result()."""
    out = {}
    for n, fn in _CHECKS.items():
        r = fn()
        listed = len(r['fail_reasons'])
        counted = r['fail_count']
        if listed != counted:
            raise AssertionError(
                f"{n}: failure records disagree -- fail_reasons has {listed} "
                f"entries, the independent counter says {counted}")
        r['passed'] = (counted == 0)
        out[n] = r
    return out


if __name__ == '__main__':
    import sys
    bad = False
    for n, r in run_all().items():
        print(r['name'], '::', r['epistemic'], '::',
              'PASS' if r['passed'] else 'FAIL',
              f"({r['leg_count']} legs)")
        if not r['passed']:
            bad = True
            for f in r['fail_reasons'][:20]:
                print('  -', f)
    sys.exit(1 if bad else 0)
