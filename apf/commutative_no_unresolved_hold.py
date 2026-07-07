"""No coherent hold is admissible-visible in a commutative algebra.

L_commutative_no_unresolved_hold.  For a commutative *-algebra A of
projectors on a finite-dimensional space -- the admissibility algebra of a
Sep-branch interface, where T_no_IJC_no_noncommutativity [P_structural]
exhibits [E_d, E_joint] = 0 -- the "maintained unresolved hold" of
alternatives that structure-building search would need is invisible to every
observable in A:

  (i)  [P_math] every pure state (character) of A assigns each generator
       projector a definite value in {0,1}: chi(E)^2 = chi(E^2) = chi(E)
       forces chi(E) in {0,1}.  There are no admissible superposed VALUES.

  (ii) [P_math] for ANY state rho, the A-conditional expectation (dephasing)
       D(rho) = sum_pi Q_pi rho Q_pi over the minimal joint spectral
       projections {Q_pi} satisfies Tr(rho A) = Tr(D(rho) A) for every A in
       A.  D is trace-preserving and idempotent (a genuine conditional
       expectation).  The off-diagonal "hold" content of rho is invisible to
       the whole algebra.

  (iii)[P_math] any observable W distinguishing rho from D(rho)
       (Tr(W rho) != Tr(W D(rho))) is NOT in the COMMUTANT of A -- it has
       nonzero off-diagonal against {Q_pi}.  In the MASA case (all minimal
       joint spectral projections rank 1 -- the physically relevant
       distinct-minimal-distinctions case) commutant == algebra, so a
       coherence-witness satisfies [W, E] != 0 for a generator E: it is a
       non-commuting element.

APPLICATION (the [P_structural] bridge -- rides the IJC dichotomy, NOT part
of the [P_math] gate).  In branch Sep the admissibility algebra is
commutative (T_no_IJC), so by (i)-(iii) no ADMISSIBLE observable witnesses a
coherent hold; a coherence-witness is exactly a non-commuting element =
pool-sector engagement F_Pi != 0 = branch IJC, absent in Sep.  A maintained
unresolved hold of alternatives is therefore operationally identical to a
definite-assignment mixture: it does NO admissible building work the serial
route lacks.  This is what K2's drawn clause (in check_T_gapless_serial_floor)
reads off the Sep branch -- a STRUCTURAL READING of the Sep antecedent, not
an independent constitutive derivation (so the kernel STAYS [P_structural];
this lemma does not lift it to [P] -- the Sep-branch antecedent is the wall).

GRADE [P_math].  Legs (i)-(iii) are exact finite-dimensional linear algebra
with no substrate encoding; witnessed on genuinely NON-DIAGONAL rational
projector algebras (a dim-3 MASA + a dim-4 NON-MASA control that exhibits the
commutant != algebra distinction).  All arithmetic exact Fraction/integer.
The application clause is [P_structural] and is REPORTED, not gated.

Hostile audit LAND-WITH-FIXES 0.86 (MAJOR-A commutant-vs-algebra scope +
MAJOR-B "derived"->"structural reading" + minor redundant-I, all carried).
Lane records: The Turning/zipper_slack_necessity_2026-07-07/
(walk_no_unresolved_hold.py, 41 checks; NOTE v0.2; HOSTILE_AUDIT_B report).
"""

from fractions import Fraction as F


def _mat(rows):
    return [[F(x) for x in r] for r in rows]


def _eye(n):
    return [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]


def _mm(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)]
            for i in range(n)]


def _add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _scal(c, A):
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _tr(A):
    return sum(A[i][i] for i in range(len(A)))


def _eq(A, B):
    return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A[0])))


def _T(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def _comm(A, B):
    return _sub(_mm(A, B), _mm(B, A))


def _is0(A):
    return all(A[i][j] == 0 for i in range(len(A)) for j in range(len(A[0])))


def _rank1(v):
    n = len(v)
    vv = sum(x * x for x in v)
    return [[F(v[i] * v[j], 1) / vv for j in range(n)] for i in range(n)]


def check_L_commutative_no_unresolved_hold():
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)

    # dim-3 MASA witness: two orthogonal rational rank-1 projectors
    P1 = _rank1([1, 1, 0])
    P2 = _rank1([1, -1, 0])
    P0 = _sub(_sub(_eye(3), P1), P2)
    SPEC = [P1, P2, P0]
    GENS = [P1, P2]

    # (0) commuting non-diagonal projector algebra
    for P in SPEC:
        ck(_eq(_mm(P, P), P), "projector idempotent")
        ck(_eq(_T(P), P), "self-adjoint")
    ck(_is0(_comm(P1, P2)), "[P1,P2]=0 (commutative, non-diagonal)")
    ck(_eq(_add(_add(P1, P2), P0), _eye(3)), "resolution of identity")
    for i in range(3):
        for j in range(3):
            if i != j:
                ck(_is0(_mm(SPEC[i], SPEC[j])), "spectral orthogonality")

    # (i) characters are {0,1}
    for Q in SPEC:
        trq = _tr(Q)
        for E in GENS:
            val = _tr(_mm(Q, E)) / trq
            ck(val in (F(0), F(1)), "character value in {0,1}")

    # (ii) dephasing invariance on the algebra
    def dephase(rho, spec):
        n = len(rho)
        out = [[F(0)] * n for _ in range(n)]
        for Q in spec:
            out = _add(out, _mm(_mm(Q, rho), Q))
        return out

    rho = _add(_scal(F(2, 3), _rank1([2, 1, 1])), _scal(F(1, 3), _rank1([1, 0, 1])))
    ck(_tr(rho) == 1, "rho trace-1")
    Drho = dephase(rho, SPEC)
    ck(_tr(Drho) == 1, "D(rho) trace-preserving")
    ck(_eq(dephase(Drho, SPEC), Drho), "D idempotent (conditional expectation)")
    ck(not _eq(rho, Drho), "rho has genuine off-diagonal hold content")
    for A in SPEC:                                  # MASA: SPEC spans the algebra
        ck(_tr(_mm(rho, A)) == _tr(_mm(Drho, A)), "hold invisible to the algebra")

    # (iii) a distinguishing observable is off-commutant; MASA => non-commuting
    M = _mat([[1, 2, 3], [0, 1, 1], [2, 0, 1]])
    W = _add(_mm(_mm(P1, M), P0), _mm(_mm(P0, _T(M)), P1))
    ck(_eq(_T(W), W), "W self-adjoint")
    ck(_tr(_mm(W, rho)) != _tr(_mm(W, Drho)), "W distinguishes rho from D(rho)")
    ck(any(not _is0(_comm(W, Q)) for Q in SPEC), "W outside the commutant")
    ck(all(_tr(Q) == 1 for Q in SPEC), "dim-3 witness is a MASA")
    ck(any(not _is0(_comm(W, E)) for E in GENS),
       "MASA: coherence-witness is non-commuting (= branch IJC)")

    # dim-4 NON-MASA control: commutant strictly larger than the algebra
    Pa = _mat([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    Pb = _mat([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    Pc = _sub(_sub(_eye(4), Pa), Pb)
    ck(_is0(_comm(Pa, Pb)), "4x4 generators commute")
    ck(_tr(Pa) == 2 and _tr(Pb) == 2, "rank-2 -> NON-MASA")
    rho4 = _rank1([2, 1, 1, 1])
    D4 = dephase(rho4, [Pa, Pb])
    for A in [Pa, Pb, _eye(4)]:
        ck(_tr(_mm(rho4, A)) == _tr(_mm(D4, A)),
           "4x4 NON-MASA: dephasing invariance on the algebra (general fact)")
    Wc = _mat([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    ck(_is0(_comm(Wc, Pa)) and _is0(_comm(Wc, Pb)), "Wc in the commutant")
    zero4 = [[F(0)] * 4 for _ in range(4)]
    ck(not any(_eq(Wc, A) for A in [Pa, Pb, Pc, _eye(4), zero4]),
       "Wc not in the 2-dim algebra -> commutant != algebra (non-MASA)")

    passed = not fails
    return {
        'name': 'L_commutative_no_unresolved_hold',
        'epistemic': 'P_math',
        'passed': passed,
        'tier': 4,
        'key_result': (
            'commutative projector algebra: (i) pure states are {0,1} '
            'assignments; (ii) A-dephasing D(rho)=sum Q_pi rho Q_pi is '
            'invariant on the algebra (hold invisible); (iii) any '
            'distinguishing observable is off-commutant, MASA => non-commuting '
            '[P_math, exact, non-diagonal + non-MASA control]. APPLICATION '
            '[P_structural, reported]: in Sep (commutative, T_no_IJC) no '
            'admissible observable witnesses a coherent hold -- a hold is '
            'operationally identical to a definite mixture; a coherence-witness '
            '= non-commuting element = branch IJC (F_Pi != 0). This is the '
            'STRUCTURAL READING K2 reads off the Sep antecedent; it does NOT '
            'lift check_T_gapless_serial_floor to [P] (the Sep antecedent is '
            'the principled wall).'
        ),
        'dependencies': [],
        'cross_refs': ['T_no_IJC_no_noncommutativity', 'T_IJC_dichotomy',
                       'T_gapless_serial_floor'],
        'artifacts': {
            'witness_masa': 'dim-3, orthogonal rational rank-1 projectors (MASA)',
            'witness_nonmasa': 'dim-4 rank-2 control (commutant != algebra)',
            'grade_gate': '[P_math] on legs (i)-(iii); application clause [P_structural] reported-not-gated',
            'kernel_effect': 'K2 drawn clause = structural reading (not derived); kernel stays [P_structural]',
            'audit': 'LAND-WITH-FIXES 0.86; MAJOR-A/B + minor carried',
            'note_home': 'The Turning/zipper_slack_necessity_2026-07-07/',
        },
        'fail_reasons': fails,
    }


_CHECKS = {'L_commutative_no_unresolved_hold': check_L_commutative_no_unresolved_hold}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == '__main__':
    import sys
    r = check_L_commutative_no_unresolved_hold()
    print(r['name'], r['epistemic'], 'PASS' if r['passed'] else 'FAIL')
    for f in r['fail_reasons']:
        print('  -', f)
    sys.exit(0 if r['passed'] else 1)
