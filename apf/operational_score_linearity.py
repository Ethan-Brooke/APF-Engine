"""Executed derivation of operational score linearity on M_2(C).

FORTIFIED 2026-07-21 per the cold audit (COLD_AUDIT_v06_v08_foundation.md,
verdict REDUCE 0.75).  Every MAJOR carried at statement level:

* MAJOR-1: the load-bearing total-probability-for-scores premise is now the
  NAMED leaf CLASSICAL_SCORE_TOTALITY, wired into the derivation engine, the
  dependency contract, the manifest, and the manuscript.  Linearity is
  obtained from classical mixing + additivity + THIS leaf, not from mixing
  alone.
* MAJOR-2/4: witness-theater replaced by the executed derivation.  The
  affinity and additivity steps are executed as exact linear ENTAILMENT over
  named axiom instances (goal in the row space of the axioms, Fraction
  arithmetic), and each derivation leg fails under axiom mutations, executed
  in-check.  T_LINEARITY_FORCED_ON_MATRIX_BASIS (which tested trace VALUES,
  i.e. the downstream cyclicity conclusion, under a linearity name) is
  replaced by check_T_linear_extension_determined_on_spanning_effects, which
  tests what it names: exact determination of the real-linear extension by
  scores on a spanning effect family, via an exact 4x4 solve.
* MAJOR-3: the nonlinear impostor |Tr(a)/2|^2 is an explicit executed
  adversary.  The shipped v0.8 affinity witness was degenerate (equal-score
  branches); the strengthened unequal-score battery now REJECTS the impostor
  at the affinity leg itself, as well as at additivity and scaling.
* The two constant-vs-constant checks are deleted: the contextual control is
  now an actual score object on procedures that fails MIXTURE_CONGRUENCE by
  computation, and the dependency contract is COMPUTED on a real graph with
  cycle/forbidden mutations.
* All arithmetic is exact (Fraction / Gaussian-rational pairs).  No floats.

HONEST RESIDUE (REDUCE posture, carried): the mathematics here is the
standard Busch-genre effect-algebra state-extension argument.  The packet
RE-FACTORS the CLOSED_LOOP_SCORE_LINEARITY leaf of the dense-sandwich packet
into a more primitive named operational package; it does not certify any
physical leaf and it does not force the trace.  The linear non-cyclic score
a -> a_11 satisfies every leaf below, executed in-check: cyclicity remains an
independent antecedent (the rootless-loop burden), and the identification of
loop scores of general products with the extended functional is the v0.7
burden, not this packet's.

This module certifies mathematics only.  physical_premises_certified=False.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from fractions import Fraction as F
import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DATA_MANIFEST_PATH = PACKAGE_ROOT / "DATA" / "reduced_leaf_manifest.json"

# Bank-landing embed (v24.3.434): the reduced-leaf manifest as a module
# constant, byte-equivalent in content to DATA/reduced_leaf_manifest.json.
# The packet JSON remains the provenance copy; when the packet DATA/ layout
# is present it is preferred, so the standalone packet is unchanged in
# behavior.  In the bank tree (no DATA/) the embedded constant serves.
REDUCED_LEAF_MANIFEST: Dict[str, object] = {'version': '0.8-fortified-2026-07-21',
     'derived_and_removed_as_independent_leaves': ['CLOSED_LOOP_SCORE_LINEARITY',
                                                   'COMPLEX_SCORE_LINEARITY'],
     'reduction_scope_note': 'The reduction RE-FACTORS the linearity leaf into '
                             'the primitive package below; it does not certify '
                             "it. The dense-sandwich packet's "
                             'CLOSED_LOOP_SCORE_LINEARITY leaf is discharged only '
                             'conditionally on this full named set, including '
                             'CLASSICAL_SCORE_TOTALITY (added by the 2026-07-21 '
                             'fortification: the completed score of a classically '
                             'randomized procedure is the classical average of '
                             'the branch conditional scores -- total probability '
                             'for scores; it was load-bearing and unnamed in the '
                             'shipped v0.8).',
     'primitive_operational_leaves': ['CLASSICAL_RANDOMIZATION',
                                      'MIXTURE_CONGRUENCE',
                                      'CLASSICAL_SCORE_TOTALITY',
                                      'MUTUALLY_EXCLUSIVE_COMPLETED_RECORDS',
                                      'RECORD_COARSE_GRAINING',
                                      'ORDER_UNIT_NORMALIZATION',
                                      'OPERATIONAL_CLOSURE_OR_CONTINUITY',
                                      'ORIENTED_J_COMPLEXIFICATION'],
     'convenience_axioms': ['MUTUALLY_EXCLUSIVE_COMPLETED_RECORDS',
                            'RECORD_COARSE_GRAINING'],
     'convenience_note': 'The two record leaves are derivable from '
                         'CLASSICAL_RANDOMIZATION + MIXTURE_CONGRUENCE + '
                         'CLASSICAL_SCORE_TOTALITY + s(0)=0 (executed in '
                         'check_T_additivity_derivation_executed); they are '
                         'retained as named convenience axioms per audit F3.',
     'imported_structural_input': 'ORIENTED_J_COMPLEXIFICATION is supplied by the '
                                  'graded-orientation theorem line (fortified '
                                  'intake packet), not by this note.',
     'transit_caveat': 'The identification of the physical loop score of general '
                       'products ab with the extended functional L(ab) is the '
                       'v0.7 rootless-loop burden (ROOTLESS_LOOP_CYCLICITY + '
                       'DAGGER_SANDWICH_REALIZATION); this packet supplies '
                       'neither.',
     'physical_premises_certified': False}


def _load_reduced_leaf_manifest() -> Dict[str, object]:
    """Prefer the packet DATA copy when present (packet layout unchanged);
    fall back to the embedded bank-landing constant otherwise."""
    if DATA_MANIFEST_PATH.is_file():
        return json.loads(DATA_MANIFEST_PATH.read_text(encoding="utf-8"))
    return dict(REDUCED_LEAF_MANIFEST)

Gaussian = Tuple[F, F]
GMatrix = Tuple[Tuple[Gaussian, ...], ...]

ZERO_G: Gaussian = (F(0), F(0))
ONE_G: Gaussian = (F(1), F(0))
I_G: Gaussian = (F(0), F(1))


def _g(re, im=0) -> Gaussian:
    return (F(re), F(im))


def _gadd(x: Gaussian, y: Gaussian) -> Gaussian:
    return (x[0] + y[0], x[1] + y[1])


def _gsub(x: Gaussian, y: Gaussian) -> Gaussian:
    return (x[0] - y[0], x[1] - y[1])


def _gmul(x: Gaussian, y: Gaussian) -> Gaussian:
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def _gscale(s: F, x: Gaussian) -> Gaussian:
    return (s * x[0], s * x[1])


def _gconj(x: Gaussian) -> Gaussian:
    return (x[0], -x[1])


def _gabs2(x: Gaussian) -> F:
    return x[0] * x[0] + x[1] * x[1]


def _mat(rows) -> GMatrix:
    return tuple(tuple(x for x in row) for row in rows)


def _madd(a: GMatrix, b: GMatrix) -> GMatrix:
    return _mat([[_gadd(a[i][j], b[i][j]) for j in range(2)] for i in range(2)])


def _msub(a: GMatrix, b: GMatrix) -> GMatrix:
    return _mat([[_gsub(a[i][j], b[i][j]) for j in range(2)] for i in range(2)])


def _mscale(s: F, a: GMatrix) -> GMatrix:
    return _mat([[_gscale(s, a[i][j]) for j in range(2)] for i in range(2)])


def _mgscale(z: Gaussian, a: GMatrix) -> GMatrix:
    return _mat([[_gmul(z, a[i][j]) for j in range(2)] for i in range(2)])


def _mmul(a: GMatrix, b: GMatrix) -> GMatrix:
    out = []
    for i in range(2):
        row = []
        for j in range(2):
            acc = ZERO_G
            for k in range(2):
                acc = _gadd(acc, _gmul(a[i][k], b[k][j]))
            row.append(acc)
        out.append(row)
    return _mat(out)


def _mdag(a: GMatrix) -> GMatrix:
    return _mat([[_gconj(a[j][i]) for j in range(2)] for i in range(2)])


def _mtrace(a: GMatrix) -> Gaussian:
    return _gadd(a[0][0], a[1][1])


I2: GMatrix = _mat([[ONE_G, ZERO_G], [ZERO_G, ONE_G]])
ZERO2: GMatrix = _mat([[ZERO_G, ZERO_G], [ZERO_G, ZERO_G]])
E11: GMatrix = _mat([[ONE_G, ZERO_G], [ZERO_G, ZERO_G]])
E12: GMatrix = _mat([[ZERO_G, ONE_G], [ZERO_G, ZERO_G]])
E21: GMatrix = _mat([[ZERO_G, ZERO_G], [ONE_G, ZERO_G]])
E22: GMatrix = _mat([[ZERO_G, ZERO_G], [ZERO_G, ONE_G]])
PAULI_X: GMatrix = _mat([[ZERO_G, ONE_G], [ONE_G, ZERO_G]])
PAULI_Y: GMatrix = _mat([[ZERO_G, (F(0), F(-1))], [I_G, ZERO_G]])

# Hermitian basis of A_sa (real dimension 4).
SA_BASIS: Tuple[GMatrix, ...] = (E11, E22, PAULI_X, PAULI_Y)
SA_BASIS_NAMES = ("E11", "E22", "X", "Y")

# Spanning effect family: four exact projectors.
EFF_F1 = E11
EFF_F2 = E22
EFF_F3 = _mscale(F(1, 2), _madd(I2, PAULI_X))
EFF_F4 = _mscale(F(1, 2), _madd(I2, PAULI_Y))
SPANNING_EFFECTS: Tuple[GMatrix, ...] = (EFF_F1, EFF_F2, EFF_F3, EFF_F4)


def _sa_coords(h: GMatrix) -> Tuple[F, F, F, F]:
    """Exact coordinates of a Hermitian matrix in SA_BASIS."""
    if h != _mdag(h):
        raise ValueError("not Hermitian")
    a = h[0][0][0]
    d = h[1][1][0]
    x = h[0][1][0]      # coefficient of PAULI_X
    y = -h[0][1][1]     # coefficient of PAULI_Y  (h01 = x - i y)
    return (a, d, x, y)


def _sa_build(c: Sequence[F]) -> GMatrix:
    out = ZERO2
    for coef, b in zip(c, SA_BASIS):
        out = _madd(out, _mscale(coef, b))
    return out


# ---------------------------------------------------------------------------
# Exact linear algebra over Fractions
# ---------------------------------------------------------------------------


def _rank(rows: Iterable[Sequence[F]]) -> int:
    work = [[F(x) for x in row] for row in rows]
    work = [row for row in work if any(row)]
    if not work:
        return 0
    r = 0
    ncols = len(work[0])
    for col in range(ncols):
        pivot = next((i for i in range(r, len(work)) if work[i][col] != 0), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        pv = work[r][col]
        work[r] = [x / pv for x in work[r]]
        for i in range(len(work)):
            if i != r and work[i][col] != 0:
                q = work[i][col]
                work[i] = [a - q * b for a, b in zip(work[i], work[r])]
        r += 1
    return r


def _solve(mat: Sequence[Sequence[F]], rhs: Sequence[F]) -> Optional[List[F]]:
    """Solve square system exactly; None if singular."""
    n = len(mat)
    work = [[F(x) for x in row] + [F(rhs[i])] for i, row in enumerate(mat)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if work[i][col] != 0), None)
        if pivot is None:
            return None
        work[col], work[pivot] = work[pivot], work[col]
        pv = work[col][col]
        work[col] = [x / pv for x in work[col]]
        for i in range(n):
            if i != col and work[i][col] != 0:
                q = work[i][col]
                work[i] = [a - q * b for a, b in zip(work[i], work[col])]
    return [work[i][n] for i in range(n)]


def _entailed(axioms: Sequence[Sequence[F]], goal: Sequence[F]) -> bool:
    """Exact linear entailment: goal is in the row span of the axioms."""
    base = _rank(axioms)
    return _rank(list(axioms) + [list(goal)]) == base


# ---------------------------------------------------------------------------
# Score models (exact)
# ---------------------------------------------------------------------------


def score_normalized_trace(a: GMatrix) -> Gaussian:
    """Consistency-witness model score (the downstream trace)."""
    return _gscale(F(1, 2), _mtrace(a))


def score_coordinate_11(a: GMatrix) -> Gaussian:
    """Linear, positive, normalized, NON-cyclic score."""
    return a[0][0]


def score_nonlinear_impostor(a: GMatrix) -> F:
    """|Tr(a)/2|^2 -- the audit's adversary, exact."""
    return _gabs2(_gscale(F(1, 2), _mtrace(a)))


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


# ---------------------------------------------------------------------------
# Leaves and dependency graph (computed, not hardcoded booleans)
# ---------------------------------------------------------------------------

REMAINING_PHYSICAL_LEAVES: Tuple[str, ...] = (
    "CLASSICAL_RANDOMIZATION",
    "MIXTURE_CONGRUENCE",
    "CLASSICAL_SCORE_TOTALITY",
    "MUTUALLY_EXCLUSIVE_COMPLETED_RECORDS",
    "RECORD_COARSE_GRAINING",
    "ORDER_UNIT_NORMALIZATION",
    "OPERATIONAL_CLOSURE_OR_CONTINUITY",
    "ORIENTED_J_COMPLEXIFICATION",
)

# Derivable from randomization + congruence + totality + s(0)=0 (executed in
# check_T_additivity_derivation_executed); retained as named convenience
# axioms per the audit's F3.
CONVENIENCE_AXIOMS: Tuple[str, ...] = (
    "MUTUALLY_EXCLUSIVE_COMPLETED_RECORDS",
    "RECORD_COARSE_GRAINING",
)

DEPENDENCY_GRAPH: Dict[str, Tuple[str, ...]] = {
    "REAL_AFFINITY": (
        "CLASSICAL_RANDOMIZATION",
        "MIXTURE_CONGRUENCE",
        "CLASSICAL_SCORE_TOTALITY",
    ),
    "FINITE_ADDITIVITY": ("REAL_AFFINITY", "ORDER_UNIT_NORMALIZATION"),
    "POSITIVE_EXTENSION": (
        "REAL_AFFINITY",
        "FINITE_ADDITIVITY",
        "ORDER_UNIT_NORMALIZATION",
        "OPERATIONAL_CLOSURE_OR_CONTINUITY",
    ),
    "REAL_LINEAR_FUNCTIONAL": ("POSITIVE_EXTENSION",),
    "COMPLEX_EXTENSION": ("REAL_LINEAR_FUNCTIONAL", "ORIENTED_J_COMPLEXIFICATION"),
    "TRACE_BORN": (
        "COMPLEX_EXTENSION",
        "ROOTLESS_LOOP_CYCLICITY",
        "DAGGER_SANDWICH_REALIZATION",
    ),
}

FORBIDDEN_DEPENDENCIES = {
    "G_HOLD_EXACT",
    "STATE_COMPLETION",
    "MEASUREMENT_COMPLETION",
    "PROCESS_SATURATION",
}


def _all_nodes(graph: Mapping[str, Sequence[str]]) -> set:
    return set(graph) | {d for deps in graph.values() for d in deps}


def _roots(graph: Mapping[str, Sequence[str]]) -> Tuple[str, ...]:
    nodes = set(graph)
    return tuple(sorted({d for deps in graph.values() for d in deps if d not in nodes}))


def _deps(graph: Mapping[str, Sequence[str]], node: str) -> set:
    out: set = set()
    todo = list(graph.get(node, ()))
    while todo:
        d = todo.pop()
        if d in out:
            continue
        out.add(d)
        todo.extend(graph.get(d, ()))
    return out


def _cycle(graph: Mapping[str, Sequence[str]]) -> Optional[Tuple[str, ...]]:
    nodes = _all_nodes(graph)
    state = {n: 0 for n in nodes}
    stack: List[str] = []

    def dfs(n: str) -> Optional[Tuple[str, ...]]:
        if state[n] == 1:
            i = stack.index(n)
            return tuple(stack[i:] + [n])
        if state[n] == 2:
            return None
        state[n] = 1
        stack.append(n)
        for d in graph.get(n, ()):
            c = dfs(d)
            if c is not None:
                return c
        stack.pop()
        state[n] = 2
        return None

    for n in sorted(nodes):
        c = dfs(n)
        if c is not None:
            return c
    return None


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def check_T_affinity_derivation_executed() -> Check:
    """Executed derivation: TOTALITY + CONGRUENCE (via RANDOMIZATION) entail
    affinity, as exact linear entailment; each axiom mutation breaks it.

    Atoms per weight lambda:  [ s(proc), s(e), s(f), s(mix) ].
    TOTALITY:   s(proc) - lam*s(e) - (1-lam)*s(f) = 0
                (the completed score of the classically randomized procedure
                is the classical average of the branch conditional scores --
                the NAMED leaf CLASSICAL_SCORE_TOTALITY)
    CONGRUENCE: s(proc) - s(mix) = 0
                (CLASSICAL_RANDOMIZATION represents proc by the effect
                lam*e+(1-lam)*f; MIXTURE_CONGRUENCE gives it that score)
    GOAL:       s(mix) - lam*s(e) - (1-lam)*s(f) = 0.
    """
    fails: List[str] = []
    lambdas = (F(1, 2), F(3, 8), F(1, 4), F(5, 16))
    for lam in lambdas:
        totality = [F(1), -lam, -(1 - lam), F(0)]
        congruence = [F(1), F(0), F(0), F(-1)]
        goal = [F(0), -lam, -(1 - lam), F(1)]
        if not _entailed([totality, congruence], goal):
            fails.append(f"affinity not entailed at lambda={lam}")
        # Mutations: dropping either axiom must break the derivation.
        if _entailed([congruence], goal):
            fails.append(f"affinity wrongly entailed without CLASSICAL_SCORE_TOTALITY at lambda={lam}")
        if _entailed([totality], goal):
            fails.append(f"affinity wrongly entailed without MIXTURE_CONGRUENCE at lambda={lam}")
    # The congruence antecedent is a matrix fact: the represented effects of
    # the two branch orders coincide, exactly.
    lam = F(3, 8)
    mix_ab = _madd(_mscale(lam, E11), _mscale(1 - lam, EFF_F3))
    mix_ba = _madd(_mscale(1 - lam, EFF_F3), _mscale(lam, E11))
    if mix_ab != mix_ba:
        fails.append("represented mixture must be order-independent")
    return Check(
        "T_AFFINITY_DERIVATION_EXECUTED",
        not fails,
        fails[0] if fails else (
            f"affinity entailed at {len(lambdas)} exact weights; "
            "derivation breaks without CLASSICAL_SCORE_TOTALITY and without "
            "MIXTURE_CONGRUENCE (mutations executed)"
        ),
    )


def check_T_additivity_derivation_executed() -> Check:
    """Executed derivation of exclusive-record additivity from affinity +
    s(0)=0, making the two record leaves convenience axioms (audit F3).

    Atoms: [ s(p1), s(p2), s(g), s(e), s(f), s(e+f), s(0) ] with
    g = (e+f)/2 represented by BOTH procedures p1 = mix(1/2; e, f) and
    p2 = mix(1/2; e+f, 0).
    """
    fails: List[str] = []
    tot1 = [F(1), F(0), F(0), F(-1, 2), F(-1, 2), F(0), F(0)]
    tot2 = [F(0), F(1), F(0), F(0), F(0), F(-1, 2), F(-1, 2)]
    cong1 = [F(1), F(0), F(-1), F(0), F(0), F(0), F(0)]
    cong2 = [F(0), F(1), F(-1), F(0), F(0), F(0), F(0)]
    zero = [F(0), F(0), F(0), F(0), F(0), F(0), F(1)]
    goal = [F(0), F(0), F(0), F(-1), F(-1), F(1), F(0)]
    axioms = [tot1, tot2, cong1, cong2, zero]
    if not _entailed(axioms, goal):
        fails.append("additivity not entailed from affinity axioms + s(0)=0")
    for i, name in ((0, "TOTALITY(p1)"), (2, "CONGRUENCE(p1)"), (3, "CONGRUENCE(p2)"), (4, "s(0)=0")):
        reduced = [row for j, row in enumerate(axioms) if j != i]
        if _entailed(reduced, goal):
            fails.append(f"additivity wrongly entailed without {name}")
    # Matrix antecedent: both procedures represent the same effect, exactly,
    # for an exclusive pair inside the effect interval.
    e, f = _mscale(F(1, 2), E11), _mscale(F(1, 2), E22)
    g1 = _madd(_mscale(F(1, 2), e), _mscale(F(1, 2), f))
    g2 = _madd(_mscale(F(1, 2), _madd(e, f)), _mscale(F(1, 2), ZERO2))
    if g1 != g2:
        fails.append("half-mixture decompositions must represent the same effect")
    return Check(
        "T_ADDITIVITY_DERIVATION_EXECUTED",
        not fails,
        fails[0] if fails else (
            "s(e+f)=s(e)+s(f) entailed from totality+congruence+s(0)=0; "
            "each axiom deletion breaks the derivation (mutations executed); "
            "record leaves are convenience axioms"
        ),
    )


def check_T_linear_extension_determined_on_spanning_effects() -> Check:
    """The real-linear extension is DETERMINED by scores on four spanning
    effects: exact 4x4 solve, invertibility, and round-trip reconstruction
    for generic non-trace functionals.  (Successor of the mislabeled
    T_LINEARITY_FORCED_ON_MATRIX_BASIS, which tested trace values.)
    """
    fails: List[str] = []
    span = [list(_sa_coords(eff)) for eff in SPANNING_EFFECTS]
    if _rank(span) != 4:
        fails.append("spanning effect family must have rank 4")
    generic_functionals = (
        (F(2, 7), F(3, 5), F(-1, 3), F(5, 11)),
        (F(0), F(1), F(1, 2), F(-2, 9)),
        (F(1, 2), F(1, 2), F(0), F(0)),  # the trace, as one instance among others
    )
    for u in generic_functionals:
        svals = [sum(c * ui for c, ui in zip(_sa_coords(eff), u)) for eff in SPANNING_EFFECTS]
        rec = _solve(span, svals)
        if rec is None or tuple(rec) != tuple(u):
            fails.append(f"reconstruction failed for u={u}")
    return Check(
        "T_LINEAR_EXTENSION_DETERMINED_ON_SPANNING_EFFECTS",
        not fails,
        fails[0] if fails else (
            "scores on {E11, E22, (I+X)/2, (I+Y)/2} determine the real-linear "
            "functional uniquely; exact solve round-trips 3 generic functionals"
        ),
    )


def check_T_extension_consistency_witnesses() -> Check:
    """Scaling-independence and difference-decomposition witnesses, run with
    a GENERIC non-trace linear functional (consistency witnesses that the
    extension formulas cohere -- not theorems about the trace), plus the
    executed failure of the nonlinear impostor on the scaling leg.
    """
    fails: List[str] = []
    u = (F(2, 7), F(3, 5), F(-1, 3), F(5, 11))

    def ell(h: GMatrix) -> F:
        return sum(c * ui for c, ui in zip(_sa_coords(h), u))

    a = _madd(_mscale(F(3), E11), E22)  # diag(3,1)
    for n, m in ((4, 8), (4, 16), (8, 32)):
        if F(n) * ell(_mscale(F(1, n), a)) != F(m) * ell(_mscale(F(1, m), a)):
            fails.append(f"scaling independence failed at n={n}, m={m}")
    # Two positive-difference decompositions of diag(2,-1).
    p1, q1 = _mscale(F(2), E11), E22
    p2 = _madd(_mscale(F(3), E11), E22)
    q2 = _madd(E11, _mscale(F(2), E22))
    if _msub(p1, q1) != _msub(p2, q2):
        fails.append("decomposition witnesses must target the same element")
    if ell(p1) - ell(q1) != ell(p2) - ell(q2):
        fails.append("difference decomposition independence failed for generic functional")
    # The nonlinear impostor violates scaling independence, executed.
    g4 = F(4) * score_nonlinear_impostor(_mscale(F(1, 4), a))
    g8 = F(8) * score_nonlinear_impostor(_mscale(F(1, 8), a))
    if g4 == g8:
        fails.append("nonlinear impostor must break scaling independence")
    return Check(
        "T_EXTENSION_CONSISTENCY_WITNESSES",
        not fails,
        fails[0] if fails else (
            f"generic-functional witnesses cohere; impostor scaling values "
            f"{g4} != {g8} (caught)"
        ),
    )


def check_T_J_complexification_unique_executed() -> Check:
    """L(x) = ell(h) + i ell(k) with x = h + i k, executed for a generic
    NON-trace real functional over exact Gaussian scalars, including
    non-Hermitian arguments; complex linearity verified exactly.
    """
    fails: List[str] = []
    u = (F(2, 7), F(3, 5), F(-1, 3), F(5, 11))

    def ell(h: GMatrix) -> F:
        return sum(c * ui for c, ui in zip(_sa_coords(h), u))

    def L(x: GMatrix) -> Gaussian:
        h = _mscale(F(1, 2), _madd(x, _mdag(x)))
        k = _mgscale((F(0), F(-1, 2)), _msub(x, _mdag(x)))
        if h != _mdag(h) or k != _mdag(k):
            raise ValueError("Cartesian decomposition must be Hermitian")
        return (ell(h), ell(k))

    battery = (E11, E12, E21, _madd(E11, _mgscale(I_G, E21)), _madd(PAULI_X, _mgscale((F(1, 2), F(1, 3)), E12)))
    scalars = (I_G, (F(3, 5), F(4, 5)), (F(-1, 2), F(1, 7)))
    for x in battery:
        for y in battery:
            if L(_madd(x, y)) != _gadd(L(x), L(y)):
                fails.append("complex additivity failed")
        for z in scalars:
            if L(_mgscale(z, x)) != _gmul(z, L(x)):
                fails.append("complex homogeneity failed")
    # Uniqueness: any complex-linear extension agreeing with ell on A_sa
    # is pinned by x = h + i k; verified on the battery via the decomposition.
    for x in battery:
        h = _mscale(F(1, 2), _madd(x, _mdag(x)))
        k = _mgscale((F(0), F(-1, 2)), _msub(x, _mdag(x)))
        if _madd(h, _mgscale(I_G, k)) != x:
            fails.append("Cartesian decomposition must reconstruct x")
    return Check(
        "T_J_COMPLEXIFICATION_UNIQUE_EXECUTED",
        not fails,
        fails[0] if fails else (
            "unique complex-linear extension verified exactly for a generic "
            "non-trace functional over Gaussian-rational scalars"
        ),
    )


def check_T_nonlinear_impostor_rejected() -> Check:
    """MAJOR-3 carried: the nonlinear normalized score |Tr(a)/2|^2 passes
    normalization but is REJECTED by the strengthened unequal-score affinity
    battery and by additivity, executed exactly."""
    fails: List[str] = []
    g = score_nonlinear_impostor
    if g(I2) != 1 or g(ZERO2) != 0:
        fails.append("impostor must pass bare normalization (that is the point)")
    # Affinity battery with UNEQUAL branch scores (the shipped v0.8 witness
    # used E11 vs E22, both scoring 1/2, and could not fail: N1).
    affinity_pairs = ((E11, ZERO2), (E11, I2), (EFF_F3, ZERO2))
    lambdas = (F(1, 2), F(3, 8))
    caught_affinity = 0
    for e, f in affinity_pairs:
        for lam in lambdas:
            mix = _madd(_mscale(lam, e), _mscale(1 - lam, f))
            if g(mix) != lam * g(e) + (1 - lam) * g(f):
                caught_affinity += 1
    if caught_affinity == 0:
        fails.append("impostor escaped the affinity battery")
    # Additivity.
    if g(_madd(E11, E22)) == g(E11) + g(E22):
        fails.append("impostor escaped additivity")
    # Degeneracy regression: the OLD witness (E11, E22, any lambda) cannot
    # catch any function of the trace; assert that fact so the battery can
    # never silently regress to it.
    lam = F(3, 8)
    old_mix = _madd(_mscale(lam, E11), _mscale(1 - lam, E22))
    old_degenerate = g(old_mix) == lam * g(E11) + (1 - lam) * g(E22)
    if not old_degenerate:
        fails.append("degeneracy regression witness changed unexpectedly")
    return Check(
        "T_NONLINEAR_IMPOSTOR_REJECTED",
        not fails,
        fails[0] if fails else (
            f"|Tr/2|^2 rejected by {caught_affinity} unequal-score affinity "
            "witnesses and by additivity; the old equal-score witness is "
            "degenerate for it (documented in-check)"
        ),
    )


def check_T_linear_noncyclic_model_within_leaves() -> Check:
    """Honesty control (REDUCE posture): the coordinate score a -> a_11 is
    linear, positive, normalized, and satisfies EVERY leaf of this packet --
    and it is not the trace.  Cyclicity is therefore genuinely external
    (the rootless-loop burden), and this packet does not force the trace."""
    fails: List[str] = []
    s = score_coordinate_11
    if s(I2) != ONE_G or s(ZERO2) != ZERO_G:
        fails.append("coordinate score must be normalized")
    lam = F(3, 8)
    for e, f in ((E11, I2), (EFF_F3, EFF_F4)):
        mix = _madd(_mscale(lam, e), _mscale(1 - lam, f))
        if s(mix) != _gadd(_gscale(lam, s(e)), _gscale(1 - lam, s(f))):
            fails.append("coordinate score must satisfy affinity")
    if s(_madd(E11, E22)) != _gadd(s(E11), s(E22)):
        fails.append("coordinate score must satisfy additivity")
    for b in (E11, E12, E21, _madd(E11, E21)):
        v = s(_mmul(_mdag(b), b))
        if v[1] != 0 or v[0] < 0:
            fails.append("coordinate score must be positive on squares")
    cyclic_broken = s(_mmul(E12, E21)) != s(_mmul(E21, E12))
    if not cyclic_broken:
        fails.append("coordinate score should fail cyclicity (it is not tracial)")
    return Check(
        "T_LINEAR_NONCYCLIC_MODEL_WITHIN_LEAVES",
        not fails,
        fails[0] if fails else (
            "a -> a_11 satisfies every v0.8 leaf yet fails cyclicity: this "
            "packet does not force the trace; cyclicity remains the v0.7 "
            "rootless-loop burden"
        ),
    )


def check_T_contextual_score_violates_congruence() -> Check:
    """Real contextual score object (not constants): a score defined on
    PROCEDURES that depends on the branch order cannot factor through the
    represented effect; the congruence violation is computed."""
    fails: List[str] = []
    lam = F(1, 2)
    e, f = E11, EFF_F3

    def represented(proc) -> GMatrix:
        w, first, second = proc
        return _madd(_mscale(w, first), _mscale(1 - w, second))

    def contextual_score(proc) -> F:
        w, first, second = proc
        # depends on presentation order, not only on the represented effect
        return F(1, 3) if first == e else F(2, 3)

    p1 = (lam, e, f)
    p2 = (lam, f, e)
    same_effect = represented(p1) == represented(p2)
    different_score = contextual_score(p1) != contextual_score(p2)
    if not same_effect:
        fails.append("procedures must represent the same effect")
    if not different_score:
        fails.append("contextual score must actually differ")
    # A congruent score cannot do this: factorization through the effect
    # forces equal values on p1, p2.  The trace model factors, executed.
    if score_normalized_trace(represented(p1)) != score_normalized_trace(represented(p2)):
        fails.append("factoring score must agree on congruent procedures")
    return Check(
        "T_CONTEXTUAL_SCORE_VIOLATES_CONGRUENCE",
        not fails,
        fails[0] if fails else (
            "order-dependent procedure score violates MIXTURE_CONGRUENCE by "
            "computation; any effect-factoring score cannot"
        ),
    )


def check_T_real_not_complex_linear_control() -> Check:
    """Re(a_11) is real-linear but not complex-linear, exact."""
    fails: List[str] = []

    def Lre(a: GMatrix) -> F:
        return a[0][0][0]

    lhs = Lre(_mgscale(I_G, E11))          # Re(i * 1) = 0
    rhs_would_be = _gmul(I_G, (Lre(E11), F(0)))  # i * 1 = i
    if (lhs, F(0)) == rhs_would_be:
        fails.append("real functional must fail complex homogeneity")
    if Lre(_madd(E11, E22)) != Lre(E11) + Lre(E22):
        fails.append("control must remain real-linear")
    return Check(
        "T_REAL_NOT_COMPLEX_LINEAR_CONTROL",
        not fails,
        fails[0] if fails else "Re(a_11): real-linear, fails L(iE11)=iL(E11) exactly",
    )


def check_T_dependency_contract_computed() -> Check:
    """The dependency contract as a computed graph: roots, acyclicity,
    forbidden-name absence, no Born-to-mixing feedback, manifest concordance,
    and executed mutations."""
    fails: List[str] = []
    graph = DEPENDENCY_GRAPH
    if _cycle(graph) is not None:
        fails.append("dependency graph must be acyclic")
    if FORBIDDEN_DEPENDENCIES & _all_nodes(graph):
        fails.append("forbidden dependency present")
    if "TRACE_BORN" in _deps(graph, "REAL_AFFINITY"):
        fails.append("Born conclusion must not feed the mixing axioms")
    if "CLASSICAL_SCORE_TOTALITY" not in graph["REAL_AFFINITY"]:
        fails.append("CLASSICAL_SCORE_TOTALITY must be an explicit affinity antecedent")
    roots = set(_roots(graph))
    expected_roots = (
        (set(REMAINING_PHYSICAL_LEAVES) - set(CONVENIENCE_AXIOMS))
        | {"ROOTLESS_LOOP_CYCLICITY", "DAGGER_SANDWICH_REALIZATION"}
    )
    if roots != expected_roots:
        fails.append(f"root inventory drift: {sorted(roots ^ expected_roots)}")
    # DATA manifest concordance (drift tripwire, fail-closed; in the bank
    # tree the embedded REDUCED_LEAF_MANIFEST constant serves).
    manifest = _load_reduced_leaf_manifest()
    manifest_leaves = set(manifest["primitive_operational_leaves"])
    if manifest_leaves != set(REMAINING_PHYSICAL_LEAVES):
        fails.append(f"module/manifest leaf drift: {sorted(manifest_leaves ^ set(REMAINING_PHYSICAL_LEAVES))}")
    if set(manifest.get("convenience_axioms", ())) != set(CONVENIENCE_AXIOMS):
        fails.append("module/manifest convenience-axiom drift")
    if manifest.get("physical_premises_certified") is not False:
        fails.append("manifest must state physical_premises_certified=false")
    # Mutations, executed.
    g1 = dict(graph)
    g1["TRACE_BORN"] = (*g1["TRACE_BORN"], "G_HOLD_EXACT")
    if not (FORBIDDEN_DEPENDENCIES & _all_nodes(g1)):
        fails.append("G_HOLD_EXACT insertion not caught")
    g2 = dict(graph)
    g2["REAL_AFFINITY"] = (*g2["REAL_AFFINITY"], "TRACE_BORN")
    if _cycle(g2) is None:
        fails.append("Born-to-affinity cycle not caught")
    g3 = dict(graph)
    g3["REAL_AFFINITY"] = tuple(d for d in g3["REAL_AFFINITY"] if d != "CLASSICAL_SCORE_TOTALITY")
    if set(_roots(g3)) == roots:
        fails.append("leaf-removal mutation not caught by root inventory")
    return Check(
        "T_DEPENDENCY_CONTRACT_COMPUTED",
        not fails,
        fails[0] if fails else (
            f"acyclic; roots={sorted(roots)}; manifest concordant; "
            "G-hold insertion, Born cycle, and leaf removal all caught"
        ),
    )


_CHECKS = (
    check_T_affinity_derivation_executed,
    check_T_additivity_derivation_executed,
    check_T_linear_extension_determined_on_spanning_effects,
    check_T_extension_consistency_witnesses,
    check_T_J_complexification_unique_executed,
    check_T_nonlinear_impostor_rejected,
    check_T_linear_noncyclic_model_within_leaves,
    check_T_contextual_score_violates_congruence,
    check_T_real_not_complex_linear_control,
    check_T_dependency_contract_computed,
)


CHECKS: Dict[str, object] = {
    fn.__name__[len("check_"):]: fn for fn in _CHECKS
}


def register(registry) -> None:
    """Bank registration (v24.3.434): stripped-``check_``-prefix keys, the
    registry convention of apf/held_holonomy.py."""
    registry.update(CHECKS)


def run_all() -> dict:
    checks = [fn() for fn in _CHECKS]
    return {
        "package": "APF Operational Score Linearity",
        "version": "0.8-fortified-2026-07-21",
        "status": "PASS" if all(c.passed for c in checks) else "FAIL",
        "physical_premises_certified": False,
        "checks": [asdict(c) for c in checks],
        "remaining_physical_leaves": list(REMAINING_PHYSICAL_LEAVES),
        "convenience_axioms": list(CONVENIENCE_AXIOMS),
        "reduction_conclusion": (
            "Standard Busch-genre state-extension mathematics, executed: the "
            "CLOSED_LOOP_SCORE_LINEARITY leaf of the dense-sandwich packet is "
            "RE-FACTORED into (not certified by) the named leaf package above, "
            "including the load-bearing CLASSICAL_SCORE_TOTALITY.  The trace is "
            "not forced here (the coordinate score satisfies every leaf); "
            "cyclicity and the loop-score identification on general products "
            "remain the v0.7 burden."
        ),
    }


if __name__ == "__main__":
    out = run_all()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
